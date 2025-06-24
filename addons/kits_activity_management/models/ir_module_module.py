from odoo import models
from odoo.addons.kits_activity_management.hooks import STORE_PROCEDURE

class ir_module_module(models.AbstractModel):
    _inherit = "ir.module.module"

    def button_immediate_upgrade(self):
        self.env.cr.execute(STORE_PROCEDURE)
        res = super(ir_module_module,self).button_immediate_upgrade()
        return res
