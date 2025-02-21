# -*- coding: utf-8 -*-
{
    'name': "TMS",
    'summary': "(transport management system)",
    'license': 'OPL-1',
    'author': "STeSI Consulting",
    'category': '',
    'version': '17.0.0.1',
    'website': "https://github.com/ingegniamo/soa1_ahmed_tms",

    # Dependencies for this module
    'depends': ['base', 'base_setup', 'mail'],
    
    # Files to load
    'data': [
        'security/tms_groups.xml',
        'security/ir.model.access.csv',
        'security/tms_security.xml',
        'views/sequence.xml',
        'views/wizard.xml',
        'views/menu_views.xml',
        'views/view.xml',
        'views/trip_type.xml',
        'views/templates.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings.xml',
        'views/trip_type_views.xml',
    ],



    'application': False,
}