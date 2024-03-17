# -*- coding: utf-8 -*-
{
    'name': "traim_associated",

    'summary': """
        Traim Association module""",

    'description': """
        This module using to management Tarim associated module
    """,

    'author': "Mohammed Almadqy",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence_file.xml',
        'views/setting_views.xml',
        'views/beneficiary_views.xml',
        'views/benficiary_request_views.xml',
        'views/program_views.xml',
        'views/main_menus.xml',
    ],
   
}
