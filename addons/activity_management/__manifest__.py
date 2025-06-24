# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
{
    'name': 'Activities Management | Activity Management | Activities Dashboard | Activity Dashboard | Schedule Activity',
    'description': """
        - Activities Management
        - Advanced Activity Management
        - Activity Dashboard
        - User wise dashboard stats
        - Administrator & User role in settings
        - List view, Kanban View, & Form View
        - Different filters in dashboard other views
        - Archive features
        - Checklist & Progress bar in activity
        - Priority in activity
        - Description & Note tab
        - Tags in activity
        - Ribbon based status
        - Auto record update based on status
        - Datatables in dashboard
        - Completed activity history
    """,
    'summary': """Odoo Acitivity/ Schedule Activity Management
    """,
    'category': 'Activity',
    'version': '1.3.2',
    'author': 'TechKhedut Inc.',
    'company': 'TechKhedut Inc.',
    'maintainer': 'TechKhedut Inc.',
    'website': "https://techkhedut.com",
    'depends': ['mail'],
    'data':[
        'security/res_groups.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'views/activity_views.xml',
        'views/activity_tag_views.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'activity_management/static/src/css/lib/daterangepicker.css',
            'activity_management/static/src/css/lib/buttons.bootstrap4.min.css',
            'activity_management/static/src/css/lib/dataTables.bootstrap4.min.css',
            'activity_management/static/src/css/lib/style.css',
            'activity_management/static/src/css/style.scss',

            'activity_management/static/src/js/lib/daterangepicker.js',
            'activity_management/static/src/js/lib/apexcharts.js',
            'activity_management/static/src/js/lib/jquery.dataTables.min.js',
            'activity_management/static/src/js/lib/dataTables.buttons.min.js',
            'activity_management/static/src/js/lib/buttons.bootstrap4.min.js',
            'activity_management/static/src/js/lib/jszip.min.js',
            'activity_management/static/src/js/lib/pdfmake.min.js',
            'activity_management/static/src/js/lib/vfs_fonts.js',
            'activity_management/static/src/js/lib/buttons.html5.min.js',
            'activity_management/static/src/js/lib/buttons.colVis.min.js',
            'activity_management/static/src/js/activity.js',
            'activity_management/static/src/xml/template.xml',
        ]
    },
    'images': ['static/description/activity-management.gif'],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 22,
    'currency': 'USD',
}
