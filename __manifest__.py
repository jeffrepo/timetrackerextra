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
        'wizard/sale_order_discount_views.xml',
        'wizard/timetrackerextra_report_commisions_views.xml',
        'report/account_invoice_report_view.xml',
        'security/timetracker_security.xml',
        'views/sale_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
    ],
    'qweb': [
    ],
    'license': 'LGPL-3',
}
