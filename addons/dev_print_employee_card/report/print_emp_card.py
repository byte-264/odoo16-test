# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class report_print_emp_card(models.AbstractModel): 
    _name = 'report.dev_print_employee_card.print_emp_card'


    def set_formate_id(self,obj,formate_id):
        obj.formate_id = formate_id and formate_id.id
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['print.employee.card'].browse(data['form'])
        return {
            'doc_ids': docs.ids,
            'doc_model': 'print.employee.card',
            'docs': docs,
            'set_formate_id': self.set_formate_id,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
