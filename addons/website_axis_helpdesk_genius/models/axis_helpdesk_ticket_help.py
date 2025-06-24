# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class axisHelpdeskTicketHelp(models.Model):
    _name = "axis.helpdesk.ticket.help"
    _description = "Helpdesk Ticket Help"

    name = fields.Char(string="Name")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company",string="Company",default=lambda self: self.env.company)