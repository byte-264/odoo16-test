# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

{
    'name': 'Employee I-Card, Employee Card, Employee Card Template',
    'version': '16.0.1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
       Odoo app allow to print Dynamic Employee Card -Inside app 5 Card Template

odoo  employee card 
employee card odoo
employee icard template 
odoo card 
odoo icard 
odoo employee card
odoo hr card
odoo employee card dynamic 
HR employee card 
Odoo HR employee card 
Manage HR employee card 
Odoo manage HR employee card
Employee card
Odoo employee card
Manage employee card
Odoo manage employee card 
Print Dynemic Employee Card
Odoo Print Dynemic Employee Card
Manage Print Dynemic Employee Card
Odoo manage Print Dynemic Employee Card
Set Font Size, Background Images, Font Color
Odoo Set Font Size, Background Images, Font Color
Manage Set Font Size, Background Images, Font Color
Odoo manage Set Font Size, Background Images, Font Color
You can Set Employee Card Width and Height
Odoo You can Set Employee Card Width and Height
Manage You can Set Employee Card Width and Height
Odoo manage You can Set Employee Card Width and Height
Design dynamically employee card
Odoo Design dynamically employee card
Manage Design dynamically employee card
Odoo manage Design dynamically employee card
Employee card format 
Odoo employee card format 
Manage employee card format 
Odoo manage employee card format
Odoo application will help to generate Employee Card Dynamically
Manage Odoo application will help to generate Employee Card Dynamically
You can set background image, Company logo, Employee image, Name and Barcode, Work Address, Home Address, Company Name, Blood Group, Employee Number, Mobile No, Employee Date of Birth etc
Odoo You can set background image, Company logo, Employee image, Name and Barcode, Work Address, Home Address, Company Name, Blood Group, Employee Number, Mobile No, Employee Date of Birth etc
Manage You can set background image, Company logo, Employee image, Name and Barcode, Work Address, Home Address, Company Name, Blood Group, Employee Number, Mobile No, Employee Date of Birth etc
Odoo manage You can set background image, Company logo, Employee image, Name and Barcode, Work Address, Home Address, Company Name, Blood Group, Employee Number, Mobile No, Employee Date of Birth etc
Employee I card 
Odoo employee I card 
Manage Employee I card 
Odoo manage Employee I card 
Employee I card Template
Odoo employee I card Template
Manage Employee I card Template
Odoo manage Employee I card Template
       
    """,
    'summary':'Print Dynamic Employee I-card 5 Card Template,employee card format,generate Employee Card Dynamically, employee icard template, employee image icard, dynamic employee icard print, employee icard multiple template, employee card, employee icard, hr card, card template',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/card_setting_views.xml',
        'wizard/print_employee_card_views.xml',
        'views/hr_employee_views.xml',
        'views/employee_sequence.xml',
        'report/employee_card_report.xml',
        'report/report_menu.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'https://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':19.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/98lXY3FSSKg',
    "license":"LGPL-3",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
