# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    crm_ticket_id = fields.Many2one('axis.helpdesk.ticket')
    crm_ticket_ids = fields.Many2many('axis.helpdesk.ticket', compute='_compute_axis_ticket_ids', string='Ticket associated to this CRM Lead')
    ticket_count = fields.Integer("Ticket Count",compute='_compute_axis_ticket_ids', groups="website_axis_helpdesk_genius.group_crm_helpdesk_ticket")
    helpdesk_ticket_id = fields.Many2one('axis.helpdesk.ticket', string="Related Helpdesk Ticket")
    helpdesk_ticket_number = fields.Char(string="Helpdesk Ticket Number", related="helpdesk_ticket_id.number",
                                         store=True)

    @api.depends('crm_ticket_id')
    def _compute_axis_ticket_ids(self):
        for lead in self:
            ticket_ids = self.env['axis.helpdesk.ticket'].search([('crm_lead_ids', '=', lead.id)])
            lead.ticket_count = len(ticket_ids)
            lead.crm_ticket_ids = ticket_ids

    def action_view_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'name': ('Helpdesk Ticket'),
            'res_model': 'axis.helpdesk.ticket',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.crm_ticket_ids.ids)],
        }

    def action_create_support_ticket(self):
        return {
            'name': 'Create Support Ticket',
            'type': 'ir.actions.act_window',
            'res_model': 'create.support.ticket.wizard',
            'view_mode': 'form',
            'context':{'crm_lead_id':self.id},
            'view_id': self.env.ref('website_axis_helpdesk_genius.create_support_ticket_wizard_form').id,
            'target': 'new',
        }
