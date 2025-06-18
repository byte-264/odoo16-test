from odoo import _,models,fields,api
from datetime import date,timedelta

class kits_activity_reminder(models.Model):
    _name = 'kits.activity.reminder'
    _description = "Activity Reminder"

    name = fields.Char(compute='compute_reminder_name',string="Name")
    time = fields.Float("Time")
    reminder_due_date = fields.Datetime("Reminder Date Time")
    type = fields.Selection([('minutes','Minutes'),('hour','Hours'),('day','Days')],string='Type',default='minutes')
    reminder_type = fields.Selection([('popup','Popup'),('mail','Mail')],string="Reminder Type",default='popup')
    activity_id = fields.Many2one('mail.activity',string='Activity')
    automation_id = fields.Many2one('base.automation',string="Automation Id")

    @api.depends('time','type','reminder_type')
    def compute_reminder_name(self):
        for record in self:
            record.name = str(record.reminder_type)+"("+str(record.time)+","+str(record.type)+")"

    def manage_reminder_datetime(self):
        if self.type == 'minutes':
            self.reminder_due_date =  self.activity_id.due_datetime- timedelta(hours=0, minutes=self.time*2)
        elif self.type == 'hour':
            self.reminder_due_date =  self.activity_id.due_datetime- timedelta(hours=self.time*2, minutes=0)
        elif self.type == 'day':
            self.reminder_due_date =  self.activity_id.due_datetime- timedelta(days=self.time*2)
    
    def manage_automation_rule(self):
        if not self.automation_id:
            model = self.env['ir.model'].sudo().search([('model','=',self._name)])
            field = self.env['ir.model.fields'].sudo().search([('model_id','=',model.id),('name','=','reminder_due_date')])
            action = self.env["ir.actions.server"].sudo().create({
                "name": "Activity Reminder Action",
                "model_id": model.id,
                "state": "code",
                "code": """model.action_notify_activity_remind(record)""",
            })
            automation = self.env["base.automation"].sudo().create({
                "name": "Activity Reminder "+str(self.activity_id.res_name),
                "trigger": "on_time",
                "model_id": model.id,
                'trg_date_id':field.id,
                'filter_pre_domain':f"[('id', '=',{self.id})]",
                'filter_domain':f"[('id', '=',{self.id})]",
                'trg_date_range':self.time,
                'trg_date_range_type':self.type,
                'state':'multi',
                'child_ids':[(6, 0, [action.id])],
            })
            self.automation_id = automation.id
        if self.automation_id:
            self.automation_id.sudo().write({
                'trg_date_range':self.time,
                'trg_date_range_type':self.type
            })

    def create(self,vals_list):
        res = super(kits_activity_reminder,self).create(vals_list)
        for reminder in res:
            if reminder.time > 0:
                reminder.manage_reminder_datetime()
                reminder.manage_automation_rule()
        return res
    
    def write(self,vals_list):
        before_time = self.time
        before_type = self.type
        before_reminder_due_date = self.reminder_due_date
        res = super(kits_activity_reminder,self).write(vals_list)
        if (self.time > 0 and before_time!=self.time) or before_type!=self.type or before_reminder_due_date != self.reminder_due_date:
            self.manage_reminder_datetime()
            self.manage_automation_rule()
        return res
    
    def unlink(self):
        self.automation_id.child_ids.sudo().unlink()
        self.automation_id.sudo().unlink()
        return super(kits_activity_reminder, self).unlink()
    
    def action_notify_activity_remind(self,records):
        for reminder in records:
            activity = reminder.activity_id
            if reminder.reminder_type == 'popup':
                message =['activity_reminder',str(activity.res_model_id.name)+ ' : ',
                        str(activity.res_name), 'Due Date : ',str(activity.date_deadline),
                        'Summary : ',str(activity.summary) if activity.summary else 'No Summary', 'Assigned To : ',activity.user_id.name,
                        str(activity.res_model), str(activity.res_id),str(activity.res_model_id.name),
                        'Due In : ',str(reminder.time)+" "+str(reminder.type)]
                
                self.env['bus.bus']._sendone(activity.user_id.partner_id, 'simple_notification', {
                    'type': 'info',
                    'title': _("Activity Reminder"+"("+(activity.activity_type_id.name)+")"),
                    'message': _(message),
                    'sticky': True
                })
            elif reminder.reminder_type == 'mail':
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                invite_template = self.env.ref('kits_activity_management.activity_reminder_mail_template')
                email_values = {
                    'subject':_("Activity Reminder"+"("+(activity.activity_type_id.name)+")"),
                    'recipient_ids':[(6, 0, [activity.user_id.partner_id.id])]
                }
                button_access={'url':base_url+f'/mail/view?model={reminder.activity_id.res_model}&res_id={reminder.activity_id.res_id}','title':"Open Document"}
                invite_template.with_context(kits_has_button_access=True,kits_button_access=button_access).send_mail(reminder.id, force_send=True, email_values=email_values,
                                        email_layout_xmlid='mail.mail_notification_layout')


    def kits_cron_unlink_automation_tules(self):
        reminders = self.env['kits.activity.reminder'].search([('automation_id','!=',False),('reminder_due_date','<',date.today())])
        for reminder in reminders:
            reminder.automation_id.child_ids.sudo().unlink()
            reminder.automation_id.sudo().unlink()