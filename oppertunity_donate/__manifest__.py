# -*- coding: utf-8 -*-
{
    'name': "Oppertunity Donate",

    'summary': """
        Traim Association module""",

    'description': """
        This module using to management Tarim associated module
    """,

    'author': "Mohammed Almadqy",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['fincial'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence_file.xml',
        'views/oppertunity_donate_views.xml',
        'views/payment_views.xml',
        'views/setting_views.xml',
        'views/transfer_fincial_views.xml',
        'views/supporter_views.xml',
        'views/beneficiary_request_views.xml',
        'views/project_views.xml',
        'views/main_menus.xml',
    ],
   
}
