from odoo import api, fields, models, _


class stock_picking_reports(models.Model):

    _inherit = 'stock.move.line'


    total_unidades_entrada = fields.Float(string="Unidades Entrada", readonly=True, store=True, compute='_calcular_total_unidades_entrada')
    total_unidades_salida = fields.Float(string="Unidades Salida", readonly=True, store=True, compute='_calcular_total_unidades_salida')
    total_unidades = fields.Float(string="Total Unidades", readonly=True, store=True,
                                          compute='_calcular_total_unidades_totales')

    @api.multi
    @api.depends('qty_done')
    def _calcular_total_unidades_entrada(self):
        if self.move_id.purchase_line_id.id != False:
            self.total_unidades_entrada = self.qty_done

    @api.multi
    @api.depends('qty_done')
    def _calcular_total_unidades_salida(self):
        if self.move_id.purchase_line_id.id == False:
           self.total_unidades_salida = self.qty_done

    @api.depends('total_unidades_entrada', 'total_unidades_salida')
    def _calcular_total_unidades_totales(self):
        t_salida = 0
        t_entrada = 0
        stock_line = self.env['stock.move.line']
        for rec in self:
            stock_ids = stock_line.search([('product_id', '=', rec.product_id.id)])
            if stock_ids:
                for stock in stock_ids:
                    if stock.move_id.purchase_line_id.id != False:
                        t_entrada += stock.qty_done
                    if stock.move_id.purchase_line_id.id == False:
                        t_salida += stock.qty_done

        rec.total_unidades = t_entrada - t_salida









