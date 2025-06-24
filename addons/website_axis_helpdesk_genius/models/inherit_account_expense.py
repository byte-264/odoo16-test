from odoo import api, fields, models


class AccountExpense(models.Model):
    _inherit = 'hr.expense'

    support_tickets = fields.Many2many('axis.helpdesk.ticket', string='Support Tickets')
    support_ticket_count = fields.Integer(string='Number of Support Tickets', compute='_compute_support_ticket_count')

    @api.depends('support_tickets')
    def _compute_support_ticket_count(self):
        for expense in self:
            expense.support_ticket_count = len(expense.support_tickets)

    def action_view_support_tickets(self):
        self.ensure_one()
        action = self.env.ref('website_axis_helpdesk_genius.axis_helpdesk_ticket_action').read()[0]
        action['domain'] = [('id', 'in', self.support_tickets.ids)]
        return action
