# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Correspondencia",
    "summary": """
        Helpdesk""",
    "version": "16.0.2.10.1",
    "license": "AGPL-3",
    "category": "After-Sales",
    "author": "AdaptiveCity, "
    "Tecnativa, "
    "ForgeFlow, "
    "C2i Change 2 Improve, "
    "Domatix, "
    "Factor Libre, "
    "SDi Soluciones, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/helpdesk",
    "depends": ["mail", "portal"],
    "data": [
        "data/helpdesk_data.xml",
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
        "views/helpdesk_ticket_templates.xml",
        "views/helpdesk_ticket_menu.xml",
        "views/helpdesk_ticket_team_views.xml",
        "views/helpdesk_ticket_stage_views.xml",
        "views/helpdesk_ticket_category_views.xml",
        "views/helpdesk_ticket_channel_views.xml",
        "views/helpdesk_ticket_tag_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_dashboard_views.xml",
    ],
    "demo": ["demo/helpdesk_demo.xml"],
    "assets": {
        "web.assets_frontend": [
            "helpdesk_mgmt/static/src/js/new_ticket.js",
        ],
    },
    "development_status": "Beta",
    "application": True,
    "installable": True,
}
