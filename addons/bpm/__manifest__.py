# -*- coding: utf-8 -*-

{
    'name': 'BPM engine (BPMN modeler)',
    'version': '1.0',
    'category': 'BPM Workflow',
    'summary': 'Provides business process modeling and execution',
    'description': """
Provides business process modeling and execution
    """,
    'author': "Svyatoslav Nadozirny",
    'website': "https://ndev.online",
    'maintainer': 'NDev',
    'depends': [
        'base_automation', 'project'
    ],
    'data': [
        'security/bpm_security.xml',
        'security/ir.model.access.csv',

        'views/process_views.xml',
        'views/project_task_views.xml',
        'views/process_instance_views.xml',
        'views/process_elements_views.xml',
        'views/todo_menus.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'bpm/static/src/xml/form_renderer.xml',
            'bpm/static/src/xml/bpmn_viewer.xml',

            'bpm/static/src/js/form_controller.js',
            'bpm/static/src/js/bpmn_viewer.js',
            'bpm/static/src/css/bpmn_viewer.css',
            'bpm/static/src/css/form_view.css',
        ],
    },
    'images': ['static/description/banner.png'],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'price': 249,
    'currency': 'EUR'

}
