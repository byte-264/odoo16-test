{'name': 'All In One Odoo Activities Management | Activity Management | Activity Dashboard | Activity Views | Activity Monitoring | Advance Activity Management',
'version': '16.0.1.1.5',
'category': 'Extra Tools',
'sequence': 1,
'summary': 'All In One Odoo Activities Management | Activity Management | Activity Dashboard | Activity Views | Activity Monitoring | Advance Activity Management\nEffortlessly manage Odoo activities with task assignments, reminders, filters, and customizable dashboards for all user roles. Simplify workflows with mass activity creation.',
'description': 'All In One Odoo Activities Management | Activity Management | Activity Dashboard | Activity Views | Activity Monitoring | Advance Activity Management\nStreamline your workflow with All In One Odoo Activities Management. Manage, track, and organize all your activities with ease. Assign tasks, set reminders, and track progress across multiple roles—User, Manager, and Administrator. With features like multi-filters, search panels, mass activities, and customizable dashboards, this app offers a comprehensive solution for efficient activity management in Odoo.',
'author': 'Keypress IT Services',
'company': 'Keypress IT services',
'maintainer': 'Keypress IT Services',
'website': 'https://www.keypress.co.in',
'data': ['security/ir.model.access.csv', 'security/groups.xml', 'security/record_rules.xml', 'security/access_rights.xml', 'data/cron.xml', 'data/mail_template.xml', 'views/activity_dashboard_view.xml', 'views/mail_activity_views.xml', 'wizard/kits_reschedule_wizard_view.xml', 'wizard/res_config_settings.xml', 'wizard/mass_activity_create_wizard_view.xml'],
'assets': {'web.assets_backend': ['kits_activity_management/static/src/scss/custom_styles.scss', 'kits_activity_management/static/src/js/activity.js', 'kits_activity_management/static/src/js/chatter.js', 'kits_activity_management/static/src/js/activity_dashboard.js', 'kits_activity_management/static/src/js/nortification.js', 'kits_activity_management/static/src/xml/chatter.xml', 'kits_activity_management/static/src/xml/activity_dashboard.xml', 'kits_activity_management/static/src/xml/nortification.xml', 'kits_activity_management/static/src/js/web_list_view_header_button.js', 'kits_activity_management/static/src/xml/web_list_view_header_button.xml']},
'depends': ['calendar', 'mail', 'base_automation'],
'installable': True,
'application': True,
'license': 'OPL-1',
'auto_install': False,
'pre_init_hook': 'kits_pre_init_hook',
'post_init_hook': 'kits_assign_current_activity_date',
'uninstall_hook': 'kits_uninstall_hook',
'currency': 'USD',
'price': 14.99,
'images': ['static/description/v16.gif'],}