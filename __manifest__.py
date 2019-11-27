# -*- coding: utf-8 -*-
{
    'name': "stock_picking_reports",

    'summary': """
        Modifica reportes de Stock Picking para mostrar mas informacion relacionada con inventario , ventas y compras""",

    'description': """
        Modifica reportes de Stock Picking para mostrar mas informacion relacionada con inventario , ventas y compras
    """,

    'author': "Fimar",
    'website': "http://www.fimarcorp.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/stock_view_move_line_tree.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}