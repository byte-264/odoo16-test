# -*- coding: utf-8 -*-

from odoo import models, fields


class MassUpdateConfig(models.Model):
    _name = 'mass.update.config'
    _description = 'Mass Update Configuration'

    name = fields.Char(
        required=True,
        string='Name',
    )
    mass_update_config_line_ids = fields.One2many(
        'mass.update.config.line',
        'update_id',
        string='Mass Update Models',
    )


class MassUpdateConfigLine(models.Model):
    _name = 'mass.update.config.line'
    _description = 'Mass Update Configuration Lines'
    _order = 'model_id'

    model_id = fields.Many2one(
        'ir.model',
        required=True,
        string='Model',
        domain=[('transient', '=', False)],
        ondelete='cascade',
    )
    update_id = fields.Many2one(
        'mass.update.config',
        string='Mass Update Id',
    )
    mass_update_wizard_id = fields.Many2one(
        'ir.actions.act_window',
        string='Mass Update Action',
    )

    def _prepare_mass_update_act_window(self):
        return {
            'name': 'Mass Update',
            'res_model': 'mass.update.wiz',
            'target': 'new',
            'binding_model_id': self.model_id.id,
            'binding_view_types': 'list',
            'view_mode': 'form',
            'target': 'new',
        }

    def add_mass_update_action(self):
        if not self.mass_update_wizard_id:
            mass_update_wizard_id = self.env['ir.actions.act_window'].create(self._prepare_mass_update_act_window())
            self.mass_update_wizard_id = mass_update_wizard_id
        else:
            return None

    def remove_mass_update_action(self):
        self.mass_update_wizard_id.unlink()

    def unlink(self):
        if self.mass_update_wizard_id:
            self.mass_update_wizard_id.unlink()
        return super(MassUpdateConfigLine, self).unlink()
