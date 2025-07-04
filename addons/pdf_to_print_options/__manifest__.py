# -*- coding: utf-8 -*-
{
    'name': 'Pdf report options',
    'summary': """This Module Provides a Direct Print Wizard Feature in Odoo""",
    'description': """
        This module in Odoo 17 adds a Direct Print Wizard with three options:
        1.Print – Instantly sends the report to the printer.
        2.Download – Downloads the report as a PDF file.
        3.Open in New Tab – Opens the report in a new browser tab for preview.
        It enhances user experience by offering flexible report printing methods.
    """,
    'version': '16.0.1.0.0',
    'price': 3.99,
    'author': 'Dhruv Radadiya',
    'category': 'Productivity',
    'images': ['static/description/heading.png'],
    'depends': ['web'],
    'data': [
        'views/ir_actions_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'report_pdf_options/static/src/**/*.xml',
            'report_pdf_options/static/src/js/PdfOptionsModal.js',
            'report_pdf_options/static/src/js/qwebactionmanager.js',
        ]
    }
}
