# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class print_employee_card(models.TransientModel):
    _name = "print.employee.card"
    _description ='Print Employee Card'
    
    
    formate_id = fields.Many2one('card.setting',string='Front Template', domain=[('page_type','=','front')])
    back_formate_id = fields.Many2one('card.setting',string='Back Template', domain=[('page_type','=','back')])
    width = fields.Float('Width', required="1", default=300)
    height = fields.Float('Height', required="1", default=500)
    
    employee_ids = fields.Many2many('hr.employee',string='Employees', required="1")

    
    @api.onchange('formate_id')
    def onchange_formate_id(self):
        if self.formate_id:
            self.width = self.formate_id.card_width
            self.height = self.formate_id.card_height
    
    def print_pdf(self):
        datas = {
		        'form': self.ids
		    }
        return self.env.ref('dev_print_employee_card.report_print_employee_card').report_action(self, data=datas)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
