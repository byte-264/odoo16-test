from odoo import models, fields, api


class MaintenanceRequestWizard(models.TransientModel):
    _name = 'maintenance.request.wizard'
    _description = 'Maintenance Request Wizard'

    name = fields.Char(string="Maintenance Req. Name", required=True)
    helpdesk_ticket_id = fields.Many2one('axis.helpdesk.ticket', string="Related Helpdesk Ticket")
    user_id = fields.Many2one('res.users', string="Responsible")
    maintenance_team_id = fields.Many2one('maintenance.team', string="Maintenance Team")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipment")

    # @api.model
    # def default_get(self, fields_list):
    #     defaults = super(MaintenanceRequestWizard, self).default_get(fields_list)
    #     if 'default_helpdesk_ticket_id' in self._context:
    #         defaults['helpdesk_ticket_id'] = self._context['default_helpdesk_ticket_id']
    #     return defaults

    def create_maintenance_request(self):
        maintenance_request_vals = {
            'name': self.name,
            'user_id': self.user_id.id,
            'maintenance_team_id': self.maintenance_team_id.id,
            'employee_id': self.employee_id.id,
            'equipment_id': self.equipment_id.id,
        }
        self.env['maintenance.request'].create(maintenance_request_vals)
        return {'type': 'ir.actions.act_window_close'}
