from odoo import fields, models, _
from odoo.exceptions import UserError


class ReassignTicketWizard(models.Model):
    _name = "reassign.ticket.wizard"

    reassign_to = fields.Selection([('user', 'User'), ('team', 'Team')], string='Reassign To')
    reassign_team_id = fields.Many2one('axis.helpdesk.ticket.team', string='Reassign Team')
    reassign_user_id = fields.Many2one('res.users', string='Reassign User')
    reassigned_ticket_id = fields.Many2one('axis.helpdesk.ticket')
    reason_details = fields.Text(string="Reason Details")

    def action_reassign(self):
        print ("----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---",self.reassigned_ticket_id)
        active_ids = self.env.context.get('active_ids')
        if active_ids and self.reassign_to:
            tickets = self.env['axis.helpdesk.ticket'].browse(active_ids)
            if not tickets.res_user_id:
                raise UserError(_('For Reassigning Ticket You Must have a User Assigned.'))
            history_records = []
            for ticket in tickets:
                reassign_data = {
                    'ticket_id': ticket.id,
                    'from_user_id': ticket.res_user_id.id,
                    'to_user_id': self.reassign_user_id.id if self.reassign_to == 'user' else False,
                    'reassign_details': self.reason_details,
                }
                history_records.append((reassign_data))
                print("HISTORY RECORDS ..............................!!!!!!!!!!!!!!!!!!!!!", history_records)

                if self.reassign_to == 'team':
                    team = self.reassign_team_id
                    assigned_user_field = self.env['ir.model.fields'].search([
                        ('model', '=', 'axis.helpdesk.ticket'),
                        ('name', '=', 'res_user_id')
                    ])
                    if assigned_user_field:
                        domain = [('id', 'in', team.res_user_ids.ids)]
                        # assigned_user_field.write({'domain': str(domain)})

                    tickets.write({'helpdesk_team_id': team.id, 'res_user_id': False})
                    available_users = team.res_user_ids

                    for ticket in tickets:
                        if ticket.res_user_id in available_users:
                            continue
                        ticket.res_user_id = False
                    template = self.env.ref('website_axis_helpdesk_genius.email_template_ticket_reassigned_to_team')
                    for member in team.res_user_ids:
                        template.send_mail(ticket.id, force_send=True, email_values={'email_to': member.email})
                    if team.team_leader_id:
                        template.send_mail(ticket.id, force_send=True,
                                           email_values={'email_to': team.team_leader_id.email})

                elif self.reassign_to == 'user':
                    user = self.reassign_user_id
                    tickets.write({'res_user_id': user.id, 'helpdesk_team_id': False})
                    template = self.env.ref('website_axis_helpdesk_genius.email_template_ticket_reassigned_to_user')
                    for ticket in tickets:
                        template.send_mail(ticket.id, force_send=True, email_values={'email_to': user.email})

            self.env['reassigned.ticket.history'].create(history_records)
        return {'type': 'ir.actions.act_window_close'}
