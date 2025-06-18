from odoo import models,fields


class kits_reschedule_wizard(models.TransientModel):
    _name = 'kits.reschedule.wizard'
    _description = "Activity Reschedule Wizard"

    reschedule_date = fields.Datetime("Reschedule Date")
    activity_id = fields.Many2one("mail.activity",string="Activity")

    def action_reschedule(self):
        self.activity_id.write({
            'date_deadline':self.reschedule_date,
            'is_reschedule':True,
            'activity_cancel':False
        })