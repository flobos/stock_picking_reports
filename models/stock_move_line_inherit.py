from odoo import api, fields, models, _


class stock_picking_reports(models.Model):

    _inherit = 'stock.move.line'

    total_unidades = fields.Float(string="Total Unidades", readonly=True, store=True, compute='_calcular_total_unidades')
    total_unidades_entrada = fields.Float(string="Unidades Entrada", readonly=True, store=True, compute='_calcular_total_unidades_entrada')
    total_unidades_salida = fields.Float(string="Unidades Salida", readonly=True, store=True, compute='_calcular_total_unidades_salida')


    @api.multi
    @api.depends('qty_done')
    def _calcular_total_unidades(self):
        stock_line = self.env['stock.move.line']
        for rec in self:

            total = 0
            stock_ids = stock_line.search([('product_id', '=', rec.product_id.id)])
            if stock_ids:
                for stock in stock_ids:
                    total += stock.qty_done
        rec.total_unidades = total

    @api.multi
    @api.depends('qty_done')
    def _calcular_total_unidades_salida(self):
        stock_line = self.env['stock.move.line']
        for rec in self:
            total = 0
            stock_ids = stock_line.search([('product_id', '=', rec.product_id.id)])
            if stock_ids:
                for stock in stock_ids:
                    stock_move = self.env['stock.move']
                    moves_ids = stock_move.search([('id', '=', stock.move_id.id)])
                    for moves in moves_ids:
                        if moves.purchase_line_id is None:
                            total += stock.qty_done
        rec.total_unidades_salida = total

    @api.multi
    @api.depends('qty_done')
    def _calcular_total_unidades_entrada(self):
        stock_line = self.env['stock.move.line']
        for rec in self:
            total = 0
            stock_ids = stock_line.search([('product_id', '=', rec.product_id.id)])
            if stock_ids:
                for stock in stock_ids:
                    stock_move = self.env['stock.move']
                    moves_ids = stock_move.search([('id', '=', stock.move_id.id)])
                    for moves in moves_ids:
                        if moves.purchase_line_id is not None:
                            total += stock.qty_done
        rec.total_unidades_entrada = total


