from odoo import models, fields


class AxisMaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    helpdesk_ticket_id = fields.Many2one('axis.helpdesk.ticket', string='Helpdesk Ticket')
