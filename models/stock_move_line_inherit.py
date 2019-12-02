from odoo import api, fields, models, _


class stock_picking_reports(models.Model):

    _inherit = 'stock.move.line'


    total_unidades_entrada = fields.Float(string="Unidades Entrada", readonly=True, store=True, compute='_calcular_total_unidades_entrada')
    total_unidades_salida = fields.Float(string="Unidades Salida", readonly=True, store=True, compute='_calcular_total_unidades_salida')
    total_unidades = fields.Float(string="Total Unidades", readonly=True, store=True,
                                          compute='_calcular_total_unidades_totales')
    precio_unidad_compra = fields.Float(string="Precio U. Compra", readonly=True, store=True,
                                          compute='_calcular_precio_unidad_compra')

    valor_costo_promedio = fields.Float(string="Costo", readonly=True, store=True,
                                          compute='_calcular_precio_costo')
    valor_debe = fields.Float(string="Debe", readonly=True, store=True,
                                          compute='_calcular_valor_debe')
    precio_unidad_venta = fields.Float(string="Precio U. Venta", readonly=True, store=True,
                                          compute='_calcular_precio_unidad_venta')

    valor_haber = fields.Float(string="Haber", readonly=True, store=True,
                              compute='_calcular_valor_haber')

    valor_saldo = fields.Float(string="Saldo", readonly=True, store=True,
                              compute='_calcular_valor_saldo')

    @api.multi
    @api.depends('valor_haber', 'valor_debe')
    def _calcular_valor_saldo(self):
        saldo = 0
        stock_line = self.env['stock.move.line']
        for rec in self:
            stock_ids = stock_line.search([('product_id', '=', rec.product_id.id)])
            if stock_ids:
                for stock in stock_ids:
                    saldo += stock.valor_debe

        rec.valor_saldo = saldo - rec.valor_haber




    @api.multi
    @api.depends('precio_unidad_venta', 'total_unidades_salida')
    def _calcular_valor_haber(self):
        for rec in self:
            if rec.move_id.purchase_line_id.id == False:
                rec.valor_haber = rec.valor_costo_promedio * rec.total_unidades_salida

    @api.multi
    @api.depends('qty_done')
    def _calcular_precio_unidad_venta(self):
        sale_order = self.env['sale.order']
        for rec in self:
            if rec.move_id.purchase_line_id.id == False:
               total = 0
               sale_ids = sale_order.search([('name', '=', rec.move_id.origin)])
               if sale_ids:
                    for sale in sale_ids:
                        for sale_line in sale.order_line:
                          if sale_line.product_id.id == rec.product_id.id:
                                total += sale_line.price_unit
                          rec.precio_unidad_venta = total

    @api.multi
    @api.depends('precio_unidad_compra', 'total_unidades_entrada')
    def _calcular_valor_debe(self):
        for rec in self:
            if rec.move_id.purchase_line_id.id != False:
                rec.valor_debe = rec.total_unidades_entrada * rec.precio_unidad_compra


    @api.multi
    @api.depends('qty_done')
    def _calcular_precio_costo(self):
        stock_line = self.env['stock.move.line']
        for rec in self:
           rec.valor_costo_promedio = rec.product_id.standard_price




    @api.multi
    @api.depends('qty_done')
    def _calcular_precio_unidad_compra(self):
        for rec in self:
            if rec.move_id.purchase_line_id.id != False:
                rec.precio_unidad_compra = rec.move_id.purchase_line_id.price_unit
            else:
                rec.precio_unidad_compra = 0


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









