# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round
import logging
import json

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            if order_line.periodo > 0:
                price = (order_line.price_unit * order_line.periodo) * (1 - (order_line.discount or 0.0) / 100.0)
                order = order_line.order_id
                return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)            
            else:
                price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
                order = order_line.order_id
                return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)
            
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    periodo = fields.Float('Periodo')
    
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','periodo')
    def _compute_amount(self):
        res = super()._compute_amount()

        for line in self:
            if line.periodo > 0:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                nuevo_precio = (line.price_unit * line.periodo) * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(nuevo_precio, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
            else:
                return res
            
    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        if self.periodo > 0:
            res['periodo'] = self.periodo
        return res
