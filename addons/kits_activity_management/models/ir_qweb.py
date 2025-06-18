from odoo import models

class IrQweb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _render(self, template, values=None, **options):
        if self.env.context.get('kits_has_button_access') and self.env.context.get('kits_button_access'):
            values['has_button_access'] = self.env.context.get('kits_has_button_access')
            values['button_access'] = self.env.context.get('kits_button_access')
        res=super(IrQweb,self)._render(template,values=values,**options)
        return res