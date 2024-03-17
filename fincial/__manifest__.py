# -*- coding: utf-8 -*-
{
    'name': "Financial",

    'summary': """
        Traim Association module""",

    'description': """
        This module using to management Tarim associated module
    """,

    'author': "Mohammed Almadqy",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['traim_association'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence_file.xml',
        'views/project_views.xml',
        'views/setting_views.xml',
        'views/executor_views.xml',
        'views/main_menus.xml',
    ],
   
}
