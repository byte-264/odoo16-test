from odoo import models, fields


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    parent_ids = fields.Many2many(
        'hr.employee.public', string='Superiors',
        compute='_compute_managers', search='_search_parent_ids',
        help="Direct and indirect managers", compute_sudo=True, recursive=True
        )
    coach_ids = fields.Many2many(
        'hr.employee.public', string='Coaches',
        compute='_compute_coach_ids', compute_sudo=True, recursive=True,
        help="Technical field to store all the coaches in coach hierarchy, i.e. coaches of coach"
        )
