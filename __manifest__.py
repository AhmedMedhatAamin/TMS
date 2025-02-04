# -*- coding: utf-8 -*-
{
    'name': "TMS",
    
    'summary': "(transport management system)",
  
    'license': 'OPL-1',

    'author': "STeSI Consulting",

    'category': '',
  
    'version': '18.0.0.1',
  
    'website': "https://github.com/ingegniamo/soa1_ahmed_tms",

    # any module necessary for this one to work correctly
    'depends': ['base'],
    
    # always loaded
    'data': [  
                'views/menu_views.xml',
                'views/view.xml',
                'views/res_partner_views.xml',
                'views/trip_type_views.xml',
        ],

    'application': False,
}
