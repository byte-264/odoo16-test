# -*- coding: utf-8 -*-
{
    'name': "Odoo to UML",

    'summary': """
        Reverse Engineering with UML diagrams.""",

    'description': """
Reverse Engineering with UML diagrams.
====================================

This is a module oriented to developers about Odoo technologies:

**Objective**:Represent the main design decisions made in the development of a module through
different UML diagrams.

Main features
---------------------------

#.  Package Diagram "Module dependencies": provides a view of the module dependencies. Admit some
     configurations to facilitate visualization:
         * Show internal structure, model classes and views.
         * Relationships between internal elements (shows relationships between classes)
         * Relations with external elements (shows relationships between classes and views with other modules)
#.  Class Diagram "Models": provides a view of the data managed in the module.

    """,
'website': "https://softwareescarlata.com/",
    'author': "David Montero Crespo",
    'website': "",
    'category': 'Tools',
    'price': 20,
    'currency': 'EUR',
    'version': '0.1',
    'depends': ['base'],
    'images': ['static/description/uml.png'],
    'data': [
        'views/inherited_module_views.xml',
'security/ir.model.access.csv',
    ]
}
