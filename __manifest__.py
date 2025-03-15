# -*- coding: utf-8 -*-
{
    'name': "Time tracker extra",

    'summary': """ Time tracker extra """,

    'description': """
        Time tracker extra
    """,

    'author': "STECHNOLOGIES",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['product','base','account','sale', 'sale_subscription','sale_management'],

    'data': [
        #'views/report.xml',
        'security/timetracker_security.xml',
        'views/sale_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
    ],
    'qweb': [
    ],
    'license': 'LGPL-3',
}
