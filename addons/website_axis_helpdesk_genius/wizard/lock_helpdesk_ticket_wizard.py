from odoo import models, fields, _
from odoo.exceptions import UserError


class LockHelpdeskTicketWizard(models.TransientModel):
    _name = 'lock.helpdesk.ticket.wizard'
    _description = 'Lock Helpdesk Ticket Wizard'

    lock_start_date = fields.Date(string="Lock Start Date")
    lock_end_date = fields.Date(string="Lock End Date")
    ticket_ids = fields.Many2many('axis.helpdesk.ticket', string="Tickets")

    def action_lock_ticket(self):
        active_ids = self.env.context.get('active_ids')
        tickets = self.env['axis.helpdesk.ticket'].browse(active_ids)

        for ticket in tickets:
            ticket.write({
                'ticket_is_locked': True,
                'ticket_locked_by': self.env.user.id,
                'lock_start_date': self.lock_start_date,
                'lock_end_date': self.lock_end_date,
            })

        return {'type': 'ir.actions.act_window_close'}
