# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
from odoo import models,fields, api


class hr_employee(models.Model):

    _inherit ='hr.employee'
    
    emp_number = fields.Char('Employee ID',required='1',readonly="1",default='/', copy=False,)
    b_group = fields.Char('Blood Group')
    
    @api.model
    def create(self, vals):
        if vals.get('emp_number',  '/') == '/':
            vals['emp_number'] = self.env['ir.sequence'].next_by_code(
                'hr.employee') or '/'
        return super(hr_employee, self).create(vals)
        
        
    def copy(self, default=None):
        if default is None:
            default = {}
        default['emp_number'] = '/'
        return super(hr_employee, self).copy(default=default)
    
    
    


    
    
    
# vim:expandtab:smartindent:tabstop=4:4softtabstop=4:shiftwidth=4:    
