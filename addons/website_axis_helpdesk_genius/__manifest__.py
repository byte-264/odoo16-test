# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Genius Helpdesk Solution help to Manage your Customer Supports Online',
    'version': '16.0.1',
    'category': 'Services/Helpdesk',
    'sequence': 110,
    'summary': 'Odoo Genius website helpdesk Ticket Support management Issue management for customer support with dashboard ticket help desk module, ticket portal, ticket management, customer helpdesk, help desk ticket, customer help desk support ticket, billing for support, timesheets, website support ticket, website help desk support online ticketing system, helpdesk module, customizable helpdesk app, Service Desk, Helpdesk with Stages, support ticket by team, flexible helpdesk module manage ticket help desk app whatsapp Help Desk Ticket Management odoo ',
    'depends': ['base_setup','mail','utm','rating','web_tour','resource','portal','project','website','hr_timesheet','web','board','account','contacts','product',
                'sale_management','hr','sale_timesheet','purchase','crm','maintenance','hr_expense'],
    'description': """Odoo website helpdesk Ticket management odoo module with version 15,14,13,12 and dashboard for your customer support ticket helpdesk module, ticket portal, ticket management, customer helpdesk, helpdesk ticket manage your customer help desk support ticket, billing for support, timesheets, website support ticket, website help desk support online ticketing system
    

Odoo Helpdesk Ticket Management App odoo 16, 15, 14, 13
================================

Features:

    - Process of customer tickets through different stages to solve them.
    - Add priorities, types, descriptions and tags to define your tickets.
    - Use the chatter to communicate additional information and ping co-workers on helpdesk tickets.
    - Enjoy the use of an adapted dashboard, and an easy-to-use kanban view to handle your ticket portal.
    - Make an in-depth analysis of your tickets through the pivot view in the reports menu.
    - Create a team and define its members, use an automatic assignment method if you wish.
    - Use a mail alias to automatically create tickets and communicate with your customers.
    - Add Service Level Agreement deadlines automatically to your Odoo website helpdesk Tickets.
    - Get customer feedback by using ratings.
    - Install additional features easily using your team form view.
    - Interactive Dashboard, Ticket filters

    """,
    "data": [  
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "data/axis_helpdesk_ticket_mail_template.xml",
        "data/helpdesk_ticket_sequence_number.xml",
        "data/helpdesk_ticket_mail_template.xml",
        "data/helpdesk_ticket_reassign_notification.xml",
        "data/helpdesk_ticket_state_change_notification.xml",
        'views/helpdesk_menu.xml',
        "views/view_axis_helpdesk_ticket_type.xml",
        "views/view_axis_helpdesk_ticket_team.xml",
        "views/view_axis_helpdesk_stage.xml",
        "views/view_axis_helpdesk_ticket.xml",
        "views/view_axis_helpdesk_ticket_category.xml",
        "views/view_axis_helpdesk_channel.xml",
        "views/view_axis_helpdesk_ticket_tag.xml",
        "views/view_axis_helpdesk_ticket_help.xml",
        "views/view_axis_helpdesk_ticket_sla_policy.xml",
        "views/view_portal_create_helpdesk_ticket.xml",
        "views/portal_template_helpdesk_ticket.xml",
        "views/helpdesk_ticket_search.xml",
        "views/view_inherit_res_config.xml",
        "views/view_inherit_res_config_setting.xml",
        "views/view_inherit_res_users.xml",

        "views/view_inherit_account_move_view.xml",
        "views/view_inherit_crm_lead_view.xml",
        "views/view_purchase_order_view.xml",
        "views/view_sale_order_view.xml",
        "views/view_axis_helpdesk_summary.xml",
        "views/view_hr_timesheet.xml",
        "views/view_helpdesk_ticket_reassign_wizard.xml",
        "views/equipment_request_view.xml",
        "views/helpdesk_asset_equipment_view.xml",
        "views/employee_travel_request_view.xml",
        "views/helpdesk_child_ticket_view.xml",
        "views/inherit_account_expense_view.xml",
        "views/view_axis_helpdesk_ticket_travel_location.xml",
        "views/helpdesk_maintenance_request_view.xml",

        "wizard/message_wizard.xml",
        "wizard/wizard_helpdesk_mass_close_ticket.xml",
        "wizard/wizard_helpdesk_merge.xml",
        "wizard/wizard_msg_whatsapp.xml",
        # "wizard/wizard_multiple_invoice_confirm.xml",
        "wizard/wizard_create_invoice_timesheet.xml",
        "wizard/support_ticket_wizard_view.xml",
        "wizard/helpdesk_ticket_child_wizard_view.xml",
        "wizard/maintenance_request_wizard_view.xml",
        "wizard/lock_helpdesk_ticket_wizard_view.xml",

        "report/report.xml",
        "report/ticket_report.xml",

    ],
    'demo': ['data/axis_helpdesk_ticket_data.xml'],
    'assets': {
        'web.assets_backend': [
            'website_axis_helpdesk_genius/static/src/xml/**/*',
            '/website_axis_helpdesk_genius/static/src/js/helpdesk_ticket_dashboard.js',
            '/website_axis_helpdesk_genius/static/src/js/helpdesk_ticket_filter_stage_dashboard.js',
            '/website_axis_helpdesk_genius/static/src/js/summary.js',
            '/website_axis_helpdesk_genius/static/src/js/board_controller.js',

            '/website_axis_helpdesk_genius/static/src/js/Chart.js',
            '/website_axis_helpdesk_genius/static/src/css/style.css',
            '/website_axis_helpdesk_genius/static/src/scss/helpdesk.scss',
        ],
        'web.assets_frontend': [
            '/website_axis_helpdesk_genius/static/src/js/portal.js',
            '/website_axis_helpdesk_genius/static/src/scss/style.scss',
        ],
        'web.assets_qweb': [
           'website_axis_helpdesk_genius/static/src/xml/helpdesk_ticket_filter_stage.xml',
           'website_axis_helpdesk_genius/static/src/xml/helpdesk_ticket_dashboard.xml',
        ],
    },

    'application': True,
    'price': 199.00,
    'currency': 'USD',
    'support': 'business@axistechnolabs.com',
    'author': 'Axis Technolabs',
    'website': 'https://www.axistechnolabs.com',
    'installable': True,
    'license': 'OPL-1',
    'images': ['static/description/Axis_Helpdesk_Genius.gif',
               'static/description/images/Banner-Img.png'],
    'live_test_url': 'https://youtu.be/iWJUZE7CXGk',
}
