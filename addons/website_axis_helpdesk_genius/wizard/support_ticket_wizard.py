from odoo import models, fields, api


class CreateSupportTicketWizard(models.TransientModel):
    _name = 'create.support.ticket.wizard'
    _description = 'Create Support Ticket Wizard'

    name = fields.Char(string="Name")
    helpdesk_team_id = fields.Many2one("axis.helpdesk.ticket.team", string="Helpdesk Team")
    category_id = fields.Many2one("axis.helpdesk.ticket.category", string="Category")
    project_id = fields.Many2one("project.project", string="Project")
    assign_to_id = fields.Many2one("res.users", string="Assign To")
    priority = fields.Selection([
        ("0", "Low"),
        ("1", "Medium"),
        ("2", "High"),
        ("3", "Very High")
    ], string="Ticket Priority", default="1")
    ticket_type_id = fields.Many2one("axis.helpdesk.ticket.type", string="Ticket Type")
    department_id = fields.Many2one("hr.department", string="Department")
    description = fields.Text(string="Description")
    # subject_type_id = fields.Many2one("axis.helpdesk.subject.type", string="Subject Type")
    crm_lead_id = fields.Many2one('crm.lead', string="Lead")

    @api.model
    def default_get(self, fields_list):
        defaults = super(CreateSupportTicketWizard, self).default_get(fields_list)
        return defaults

    def action_create_and_view_ticket(self):
        ticket_vals = {
            'name': self.name,
            'helpdesk_team_id': self.helpdesk_team_id.id,
            'res_user_id': self.assign_to_id.id,
            'priority': self.priority,
            'helpdesk_ticket_type_id': self.ticket_type_id.id,
            'description': self.description,
            'crm_lead':self.env.context['crm_lead_id'],
            'crm_lead_id':self.env.context['crm_lead_id'],
        }
        ticket = self.env['axis.helpdesk.ticket'].create(ticket_vals)
     
        crm_lead_id = self.env.context.get('crm_lead_id')
        if crm_lead_id:
            crm_lead = self.env['crm.lead'].browse(crm_lead_id)
            crm_lead.ticket_count += 1

        return {
            'name': 'Ticket',
            'view_mode': 'form',
            'res_model': 'axis.helpdesk.ticket',
            'res_id': ticket.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_create_ticket(self):
        ticket_vals = {
            'name': self.name,
            'helpdesk_team_id': self.helpdesk_team_id.id,
            'res_user_id': self.assign_to_id.id,
            'priority': self.priority,
            'helpdesk_ticket_type_id': self.ticket_type_id.id,
            'description': self.description,
            'crm_lead':self.env.context['crm_lead_id'],
            'crm_lead_id':self.env.context['crm_lead_id'],
            'crm_lead_ids':[(4, self.env.context['crm_lead_id'])]
         
        }
        ticket = self.env['axis.helpdesk.ticket'].create(ticket_vals)
        # ticket.write({'crm_lead_ids':[(4,self.env.context['crm_lead_id'])]})
        
        if self.env.context.get('crm_lead_id'):
            print ("@@@@@@@@@@@@@@@@",self.env.context.get('crm_lead_id'))
            crm_lead = self.env['crm.lead'].browse(self.env.context['crm_lead_id'])
            print ("-----CRM ACtive-----",crm_lead)
            crm_lead.sudo().write({
                'crm_ticket_id': ticket.id,
                'crm_ticket_ids': [(4, ticket.id)],
            })
            print ("================",crm_lead.crm_ticket_ids)
        return {'type': 'ir.actions.act_window_close'}
