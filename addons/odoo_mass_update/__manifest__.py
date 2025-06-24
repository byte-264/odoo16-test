# -*- coding: utf-8 -*-
{
    'name': 'Odoo Mass Update / All in one Update Records',
    'summary': 'Odoo Mass Update',
    'description': """
Odoo Mass Update
Update Multiple Records from list
Mass Update
Odoo Mass Update
Odoo Multi record update from list
Modify Record Values from list view
Update Data for selected records
Mass update at one click
Update records
Mltiple records values update
    """,
    'author': "ProsIT",
    'website': 'prosit.contactus@gmail.com',
    'license': 'OPL-1',
    'price': '35.0',
    'currency': 'USD',
    'category': 'Extra Tools',
    'version': '1.0.0',
    'images' : ['static/description/img1.jpg'],
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mass_update_data.xml',
        'views/mass_update_config_views.xml',
        'views/mass_update_history_views.xml',
        'wizard/mass_update_view.xml',
    ],
    'installable': True,
    'application': True,
}
