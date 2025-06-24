# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MassUpdateHistory(models.Model):
    _name = 'mass.update.history'
    _description = 'Mass Update History'
    _rec_name = 'model_id'

    model_id = fields.Many2one(
        'ir.model',
        string='Resource Model',
    )
    updated_on = fields.Datetime(
        string='Updated On'
    )
    updated_by = fields.Many2one(
        'res.users',
        string='Updated By'
    )
