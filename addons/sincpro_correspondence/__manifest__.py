{
'name': 'Correspondencia - Sincpro',
    'version': '16.0.1.0.0',  # Cambiar versión
    'category': 'Tools',
    'summary': 'Sistema de correspondencia para Odoo',
    'description': """
    Sistema completo de gestión de correspondencia
    """,
    "external_dependencies": {"python": ["python-docx", "sincpro-framework"]},
    "images": ["static/description/screenshot.png"],
    "price": "15.0",
    "currency": "USD",
    "license": "AGPL-3",
    "application": True,
    "author": "Sincpro S.R.L.",
    "website": "https://sincpro.com.bo",
    "depends": ["base", "mail", "hr"],
    "data": [
        "pre_configure/sequence_reason.xml",
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/correspondence_type.xml",
        "views/correspondence_actions.xml",
        "views/correspondence_reason.xml",
        "views/correspondence_document.xml",
        "views/correspondence_message.xml",
        "dialogs/assign_correspondence.xml",
        "dialogs/generate_document.xml",
        "views/app_menu.xml",
    ],
    "demo": [],
}
