from odoo import models,fields,api
from ast import literal_eval

class mass_activity_create_wizard(models.TransientModel):
    _name = 'mass.activity.create.wizard'
    _description = "Mass Activity Create Wizard"

    def default_user_id(self):
        return self.env.uid
    
    model_name = fields.Char(string = "Model")
    rec_ids = fields.Text(string="Records")
    activity_type_id = fields.Many2one("mail.activity.type",string="Activity Type")
    summary = fields.Char("Summary")
    due_date = fields.Datetime("Due Date",default=lambda self: fields.Datetime.now())
    activity_user_id = fields.Many2one("res.users",string="Assigned to",default=default_user_id)
    note = fields.Html(string="Note")
    res_model = fields.Many2one("ir.model",string="Res Model")
    activity_tags_ids = fields.Many2many("kits.activity.tags",'mass_activity_and_tags_rel','mass_activity_id','tags_id',string="Tags")
    manager_id = fields.Many2one('res.users',"Manager")

    @api.onchange('model_name')
    def compute_model_id(self):
        model_id = self.env['ir.model'].sudo().search([('model','=',self.model_name)])
        self.res_model= model_id.id

    def kits_action_schedule_activity(self):
        res_ids = literal_eval(self.rec_ids)
        for res_id in res_ids:
            self.env['mail.activity'].create({
                'summary': self.summary,
                'activity_type_id': self.activity_type_id.id,
                'note': self.note,
                'res_model_id': self.res_model.id,
                'res_id': res_id,
                'user_id': self.activity_user_id.id,
                'due_datetime':self.due_date,
                'activity_tags_ids':self.activity_tags_ids.ids,
                'manager_id':self.manager_id.id
            })
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}