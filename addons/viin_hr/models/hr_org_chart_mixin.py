import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    parent_all_count = fields.Integer(
        'Direct & Indirect Managers Count', recursive=True,
        compute='_compute_managers', store=False,
        compute_sudo=True)

    is_department_manager = fields.Boolean(string='Is Department Manager', compute='_compute_is_department_manager',
                                           search='_search_is_department_manager')

    def _compute_parent_id(self):
        """
        Override to ensure employee itself will not be applied as its manager
        If it is the manager a department, its superior deparment's manager will become its manager
        """
        super(HrEmployeeBase, self)._compute_parent_id()
        for r in self:
            if not r.parent_id or r.parent_id.id in r.department_id.manager_ids.ids:
                if isinstance(r.id, models.NewId):
                    r.parent_id = (r.department_id.manager_ids - r._origin)[:1]
                else:
                    r.parent_id = (r.department_id.manager_ids - r)[:1]

    @api.depends('parent_id', 'parent_id.parent_all_count', 'parent_id.parent_ids',
        'department_id', 'department_id.manager_id', 'department_id.manager_ids')
    def _compute_managers(self):
        # Search all departments of the employee that employee is manager
        related_departments = self.env['hr.department'].search([('manager_id', 'in', self.ids)])

        # This get all direct and indirect managers of the employee
        for r in self:
            r.parent_ids = r.parent_id
            if r.parent_id:
                r.parent_ids |= r.parent_id.parent_ids

            # sometimes we don't want department's managers
            department_manager = r._context.get('include_department_manager', True)

            # This get all direct and indirect managers of department
            if department_manager:
                department = r.department_id | related_departments.filtered(lambda dep: dep.manager_id.id == r.id)
                r.parent_ids |= self.env[self._name].browse(department.manager_ids.ids).with_prefetch(
                    prefetch_ids=(self.department_id | related_departments).manager_ids.ids
                    )
            # ensure the employee is not a superior of itself
            r.parent_ids -= r
            r.parent_all_count = len(r.parent_ids)

    @api.depends('coach_id', 'coach_id.coach_ids')
    def _compute_coach_ids(self):
        for r in self:
            r.coach_ids = r.coach_id
            if r.coach_id:
                r.coach_ids |= r.coach_id.coach_ids

    def _compute_is_department_manager(self):
        departments_vals_list = self.env['hr.department'].search_read([('manager_id', 'in', self.ids)], ['manager_id'])
        for r in self:
            if list(filter(lambda vals: vals['manager_id'][0] == r.id, departments_vals_list)):
                r.is_department_manager = True
            else:
                r.is_department_manager = False

    def _search_parent_ids(self, operator, operand):
        all_employees = self.env[self._name].search([])
        if operator in ('ilike', 'not ilike', 'in', 'not in'):
            if operator in ('in', 'not in') and isinstance(operand, list):
                domain = [('id', operator, operand)]
            else:
                domain = [('name', operator, operand)]
            list_ids = [emp.id for emp in all_employees if emp.parent_ids.filtered_domain(domain)]
        elif operator == '=':
            if operand:  # equal
                list_ids = [emp.id for emp in all_employees if emp.parent_ids == operand]
            else:  # is not set, equal = ""
                list_ids = [emp.id for emp in all_employees if not emp.parent_ids]
        elif operator == '!=':
            if operand:
                list_ids = [emp.id for emp in all_employees if emp.parent_ids != operand]
            else:  # is set
                list_ids = [emp.id for emp in all_employees if emp.parent_ids]
        else:
            raise []
        return [('id', 'in', list_ids)]

    def _search_is_department_manager(self, operator, operand):
        if not isinstance(operand, bool):
            raise UserError(_("Operation not supported"))
        departments_vals_list = self.env['hr.department'].search_read([('manager_id', '!=', False)], ['manager_id'])
        manager_ids = [vals['manager_id'][0] for vals in departments_vals_list if vals['manager_id']]
        if (operator == '=' and operand) or (operator != '=' and not operand):
            res = [('id', 'in', manager_ids)]
        else:
            res = [('id', 'not in', manager_ids)]
        return res
