# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


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
