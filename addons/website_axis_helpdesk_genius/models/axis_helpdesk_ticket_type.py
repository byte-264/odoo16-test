# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class axisTicketType(models.Model):
    _name = "axis.helpdesk.ticket.type"
    _description = "Helpdesk Ticket Type"
    # _order = 'sequence, name'

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "A type with the same name already exists."),
    ]


    def _default_domain_member_ids(self):
        return [('groups_id', 'in', self.env.ref('website_axis_helpdesk_genius.group_helpdesk_ticket_users').id)]


    name = fields.Char(string="Name",required=1)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    parent_id = fields.Many2one('axis.helpdesk.ticket.type', string='Parent',
                                help="Linking a category to its parent is used only for the reporting purpose.")
    child_ids = fields.One2many('axis.helpdesk.ticket.type', 'parent_id', string='Child Ticket Type')
    type_based_on = fields.Selection([('helpdesk_team', 'Helpdesk Team'), ('users', 'Users')], string="Type Based On",
                                     default="helpdesk_team")
    team_ids = fields.Many2many("axis.helpdesk.ticket.team",string="Helpdesk Teams")
    user_ids = fields.Many2many('res.users', string="Users", domain=lambda self: self._default_domain_member_ids())
