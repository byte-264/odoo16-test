from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_hr_allowed_fields(self):
        return self._address_fields() + ['phone', 'mobile', 'email', 'dob', 'bank_ids', 'name', 'company_id', 'type']

    def write(self, vals):
        """
        Dirty hack to allow HR officer to update employee's private address without res.users access rights error
        """
        if all(f in self._get_hr_allowed_fields() for f in vals.keys()) and self.env.user.has_group('hr.group_hr_user'):
            return super(ResPartner, self.with_context(group_hr_user_update_private_address=True)).write(vals)
        return super(ResPartner, self).write(vals)
