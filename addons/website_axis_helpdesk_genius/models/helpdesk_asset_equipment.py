from odoo import models, fields


class MyCustomEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    # equipment_line_ids = fields.One2many('equipment.request', 'equipment_request_id',
    #                                      string='Equipment Lines')
    equ_id_demo = fields.Char(string="Equipment Demo")

    def equipment_request_action_from_equipment(self):
        equipment_request_ids = self.env['equipment.request'].search([('ticket_id', '=', self.id)])
        action = self.env.ref('website_axis_helpdesk_genius.action_equipment_request').read()[0]
        action['domain'] = [('id', 'in', equipment_request_ids.ids)]
        return action

    def action_view_related_equipment(self):
        ticket_ids = self.env['axis.helpdesk.ticket'].search([('equipment_ids', 'in', self.id)])
        action = self.env.ref('website_axis_helpdesk_genius.action_helpdesk_ticket').read()[0]
        action['domain'] = [('id', 'in', ticket_ids.ids)]
        return action
