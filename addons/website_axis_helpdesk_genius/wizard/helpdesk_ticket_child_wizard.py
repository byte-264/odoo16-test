from odoo import api, fields, models


class HelpdeskTicketChildWizard(models.TransientModel):
    _name = 'helpdesk.ticket.child.wizard'
    _description = 'Helpdesk Ticket Child Wizard'

    ticket_id = fields.Many2one('axis.helpdesk.ticket', string="Parent Ticket")
    child_ticket_name = fields.Char(string="Child Ticket Name")
    child_ticket_type_id = fields.Many2one('axis.helpdesk.ticket.type', string="Ticket Type")
    child_ticket_subject = fields.Char(string="Subject")
    child_ticket_assign_to = fields.Many2one('res.users', string="Assigned To")
    child_ticket_department = fields.Many2one('axis.helpdesk.ticket.team', string="Department")
    child_ticket_priority = fields.Selection([
        ("0", ("Low")),
        ("1", ("Medium")),
        ("2", ("High")),
        ("3", ("Very High"))
    ], string="Priority", default="1")
    child_ticket_category = fields.Many2one('axis.helpdesk.ticket.type', string="Category")
    child_ticket_description = fields.Html(string="Description", required=True)

    def create_child_ticket(self):
        child_ticket_vals = {
            'name': self.child_ticket_name,
            'helpdesk_ticket_type_id': self.child_ticket_type_id.id,
            'subject': self.child_ticket_subject,
            'res_user_id': self.child_ticket_assign_to.id,
            'helpdesk_team_id': self.child_ticket_department.id,
            'priority': self.child_ticket_priority,
            'description': self.child_ticket_description,
        }
        # child_ticket = self.env['axis.helpdesk.ticket'].create(child_ticket_vals)

        # Link the created child ticket to the parent ticket
        # self.ticket_id.child_ticket_ids = [(4, child_ticket.id, 0)]

        return {'type': 'ir.actions.act_window_close'}
