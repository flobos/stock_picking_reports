# -*- coding: utf-8 -*-
from odoo import http

# class Unidad-venta(http.Controller):
#     @http.route('/unidad-venta/unidad-venta/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unidad-venta/unidad-venta/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unidad-venta.listing', {
#             'root': '/unidad-venta/unidad-venta',
#             'objects': http.request.env['unidad-venta.unidad-venta'].search([]),
#         })

#     @http.route('/unidad-venta/unidad-venta/objects/<model("unidad-venta.unidad-venta"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unidad-venta.object', {
#             'object': obj
#         })