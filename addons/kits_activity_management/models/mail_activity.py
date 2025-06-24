from odoo import _,models,fields,api,Command
from collections import defaultdict
import json

class mail_activity(models.Model):
    _inherit = 'mail.activity'
    
    state = fields.Selection(selection_add=[
        ('done','Done'),('cancel','Cancel')]
       )
    res_model_id = fields.Many2one('ir.model', 'Document Model',index=True, ondelete='cascade', required=False)

    due_datetime = fields.Datetime('Reminder date',default=lambda self: fields.Datetime.now())
    kits_ref_model = fields.Reference(selection = 'kits_select_rec_model', string = "Model")
    activity_done = fields.Boolean("Activity Done")
    activity_cancel = fields.Boolean("Activity Cancel")
    is_reschedule = fields.Boolean("Reschedule Activity")
    is_chatter = fields.Boolean("Is Chatter")
    #Add custom state because of default state not work in search panel.
    kits_state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned'),
        ('done', 'Done'),
        ('cancel','Cancel')],string="My State")
    activity_reminder_ids = fields.One2many('kits.activity.reminder','activity_id',string="Activity Reminder")
    activity_tags_ids = fields.Many2many("kits.activity.tags",'activity_and_tags_rel','activity_id','tags_id',string="Tags")
    manager_id = fields.Many2one('res.users',"Manager")
    company_id = fields.Many2one('res.company',compute="kits_get_company_id",string="Company",store=True)
    
    def kits_select_rec_model (self):
        models = self.env['ir.model'].sudo().search([('is_mail_activity','=',True),('is_mail_thread','=',True)])
        return [(model.model, model.name) for model in models]
    
    @api.depends('res_id','res_model_id','res_model')
    def kits_get_company_id(self):
        for rec in self:
            dict = {'model_name':rec.res_model,'rec_id':rec.res_id}
            json_dict=json.dumps(dict)
            self.env.cr.execute("CALL kits_get_company_id(%s)", (json_dict,))
            result = self.env.cr.fetchall()
            output = result[0][0]
            if output.get('company_id'):
                rec.company_id = output.get('company_id')
            else:
                rec.company_id = False  

    @api.model_create_multi
    def create(self,vals_list):
        if vals_list:
            if type(vals_list) == list:
                vals_list  = vals_list[0]
            if 'kits_ref_model' in vals_list.keys():
                activity_record = vals_list['kits_ref_model'].split(",")
                model = self.env['ir.model'].sudo().search([('model','=',activity_record[0])])
                vals_list['res_model_id']=model.id
                vals_list['res_model']=model.model
                vals_list['res_id']=int(activity_record[1])
        res = super(mail_activity,self).create(vals_list)
        if res:
            if 'kits_ref_model' not in vals_list.keys():
                res.kits_ref_model=res.res_model+','+str(res.res_id)
            if 'due_datetime' not in vals_list.keys():
                res.due_datetime = res.date_deadline
            elif 'date_deadline' not in vals_list.keys():
                res.date_deadline = res.due_datetime.date()
            reminder_popup_vals = {'type':'minutes','reminder_type':'popup','activity_id':res.id}
            reminder_mail_vals = {'type':'minutes','reminder_type':'mail','activity_id':res.id}
            activity_reminder_obj = self.env['kits.activity.reminder']
            activity_reminder_obj.create(reminder_popup_vals)
            activity_reminder_obj.create(reminder_mail_vals)
            res.is_chatter = False
        return res
    
    def write(self,vals_list):
        res = super(mail_activity,self).write(vals_list)
        if vals_list.get('due_datetime'):
            if self.date_deadline!=self.due_datetime.date():
                self.date_deadline = self.due_datetime.date()
            for reminder in self.activity_reminder_ids:
                if reminder.time>0:
                    reminder.manage_reminder_datetime()
        return res
    
    @api.onchange('date_deadline')
    def onchange_date_deadline(self):
        if self.date_deadline!=self.due_datetime.date():
            self.due_datetime = self.date_deadline

    @api.onchange('due_datetime')
    def onchange_date_datetime(self):
        if self.date_deadline!=self.due_datetime.date():
            self.date_deadline = self.due_datetime.date()

    def action_close_dialog(self):
        res = super(mail_activity,self).action_close_dialog()
        if self.is_chatter:
            self.is_chatter = False
            return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
        else:
            return res
        
    @api.depends('date_deadline')
    def _compute_state(self):
        for record in self.filtered(lambda activity: activity.date_deadline):
            tz = record.user_id.sudo().tz
            date_deadline = record.date_deadline
            if record.activity_done==True:
                record.state = 'done'
                record.kits_state = 'done'

            elif record.activity_cancel==True:
                record.state = 'cancel'
                record.kits_state = 'cancel'

            else:
                record.state = self._compute_state_from_date(date_deadline, tz)
                record.kits_state = record.state

    #Replace This Method For State Done Insted Of Unlink That record.
    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for model, activity_data in self._classify_by_model().items():
            records = self.env[model].browse(activity_data['record_ids'])
            for record, activity in zip(records, activity_data['activities']):
                # extract value to generate next activities
                if activity.chaining_type == 'trigger':
                    vals = activity.with_context(activity_previous_deadline=activity.date_deadline)._prepare_next_activity_values()
                    next_activities_values.append(vals)

                # post message on activity, before deleting it
                activity_message = record.message_post_with_view(
                    'mail.message_activity_done',
                    values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_activities'),
                    mail_activity_type_id=activity.activity_type_id.id,
                    attachment_ids=[Command.link(attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                )

                # Moving the attachments in the message
                # TODO: Fix void res_id on attachment when you create an activity with an image
                # directly, see route /web_editor/attachment/add
                if activity_attachments[activity.id]:
                    message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
                    if message_attachments:
                        message_attachments.write({
                            'res_id': activity_message.id,
                            'res_model': activity_message._name,
                        })
                        activity_message.attachment_ids = message_attachments
                messages += activity_message

        next_activities = self.env['mail.activity']
        if next_activities_values:
            next_activities = self.env['mail.activity'].create(next_activities_values)

        #Do State Done Insted Of Unlink That record.
        self.activity_done = True
        self._compute_state()  # will unlink activity, dont access `self` after that

        return messages, next_activities
    
    # This Method is Call When We open any record form view.
    def activity_format(self):
        self = self.filtered(lambda x: x.state not in  ['done','cancel'])
        res=super(mail_activity,self).activity_format()
        return res

    # This Method is When Cancel Activity Then Insted of unlink state cancel.
    def action_state_cancel(self):
        self.activity_cancel = True
        self._compute_state()

    def kits_mail_activity_reschedule(self):
        return {
                'name': 'Reschedule Activity',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'kits.reschedule.wizard',
                'target':'new',
                'context': {
                    "default_activity_id":self.id,
                },
            }