{
    'name': 'Partner in out mail',
    'version': '16.0.3.0.0',
    'category': 'Sales/CRM',
    'summary': 'Partner Incoming Outgoing Emails. Easy to check incoming and outgoing emails in customers, vendors or any other contacts.Track incoming and outgoing emails for partners, enhancing communication and monitoring within Odoo. partner email tracking, incoming outgoing emails Odoo, Odoo email management, track partner emails, email history tracking, customer vendor email correspondence, Odoo communication management, email monitoring Odoo, email tracking system, Odoo partner communication, Odoo email visibility, email management for businesses, improve collaboration Odoo, email tracking app Odoo, streamline partner communication, Odoo email integration',
    'description': """
    The eg_partner_in_out_mail app allows users to track and manage incoming and outgoing emails for partners directly within Odoo. 
    This feature streamlines communication by providing visibility on email correspondence with partners, making it easier to monitor interactions. 
    With the ability to track email history, users can quickly access past communications, improving collaboration and decision-making. 
    Ideal for businesses that require organized partner communication and want to enhance their email management processes.
    """,
    'author': 'INKERP',
    'website': 'https://www.inkerp.com/',
    'depends': ['base', 'mail'],

    'data': [
        'views/res_partner_view.xml',
    ],

    'images': ['static/description/banner.gif'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '5.00',
    'currency': 'EUR',
}
