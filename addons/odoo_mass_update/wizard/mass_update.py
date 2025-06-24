# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class MassUpdate(models.TransientModel):
    _name = 'mass.update.wiz'
    _description = 'Update Multiple Records at one click'

    def _get_default_model(self):
        return self.env['ir.model'].search([('model', '=', self._context.get('active_model'))], limit=1) or False

    res_model_id = fields.Many2one(
        'ir.model',
        string='Update Values on',
        required=True,
        default=_get_default_model,
    )
    mass_update_line_ids = fields.One2many(
        'mass.update.line.wiz',
        'mass_update_id',
        string="Update Value Of",
    )

    def _prepare_update_domain(self):
        return [('id', 'in', self._context.get('active_ids'))]

    def _prepare_new_update_values(self, lines):
        return {
            line.field_id.name: line['field_%s'%(line.field_id.ttype)] for line in lines
        }

    def _create_update_history(self, vals):
        vals = {
            'model_id': self.res_model_id.id,
            'updated_on': fields.Datetime.now(),
            'updated_by': self._uid,
        }
        return self.env['mass.update.history'].create(vals)

    def action_mass_update_record(self):
        if not self.mass_update_line_ids:
            raise UserError("Please add some fields and it's values to update.")
        record_ids = self.env[self.res_model_id.model].search(self._prepare_update_domain())
        get_new_value = {}
        prepare_old_value = {}
        get_new_value = self._prepare_new_update_values(self.mass_update_line_ids)
        mass_update_history_ids = self._create_update_history(get_new_value)
        record_ids.write(get_new_value)
        return True


class MassUpdateLine(models.TransientModel):
    _name = 'mass.update.line.wiz'
    _description = 'Update Value Of'

    def _get_default_model(self):
        return self.env['ir.model'].search([('model', '=', self._context.get('active_model'))], limit=1) or False

    model_id = fields.Many2one(
        'ir.model',
        string='Resource Model',
        required=True,
        default=_get_default_model,
    )
    field_id = fields.Many2one(
        'ir.model.fields',
        string='Update Value Of',
        required=True,
    )
    field_ttype = fields.Selection(
        related="field_id.ttype",
        store=True,
    )
    field_char = fields.Char(
        string='Char'
    )
    field_date = fields.Date(
        string='Date'
    )
    field_datetime = fields.Datetime(
        string='Datetime'
    )
    field_float = fields.Float(
        string='Value'
    )
    field_integer = fields.Integer(
        string='Integer'
    )
    field_html = fields.Html(
        string='Html'
    )
    field_binary = fields.Binary(
        string='Binary'
    )
    field_text = fields.Text(
        string='Text'
    )
    mass_update_id = fields.Many2one(
        'mass.update.wiz',
        string='Mass Update'
    )
    
    def _get_ttype_to_update(self):
        return ['char', 'date', 'datetime', 'float', 'html', 'integer', 'text', 'binary']

    def _get_field_domain(self):
        return [('model_id', '=', self.model_id.id), ('ttype', 'in', self._get_ttype_to_update()), ('readonly','=',False)]

    @api.onchange('model_id')
    def _onchange_model_id(self):
        return {
            'domain':{
                'field_id': self._get_field_domain(),
            },
        }
