# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round
from odoo.exceptions import UserError, ValidationError
import logging
import json

class SaleOrder(models.Model):
    _inherit = "sale.order"

    factura_numero = fields.Char(string='Numero de Factura', related='invoice_ids.name', readonly=True, store=True, index=True)
    payment_status = fields.Selection(string='Estado de Pago', related='invoice_ids.payment_state')
    supplier_ids = fields.Many2many("res.partner", string="Proveedores")
    parent_partner_id = fields.Many2one("res.partner", "Parent partner", store=True)
    
    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        for order in self:
            logging.warning(order.plan_id)
            logging.warning(order.is_subscription)
            if order.plan_id and order.is_subscription:
                logging.warning(order.next_invoice_date)
                logging.warning(order.start_date)
                last_invoice_date = order.next_invoice_date or order.start_date
                if last_invoice_date:
                    order.end_date = last_invoice_date + order.plan_id.billing_period
                else:
                    order.end_date = fields.Date.today() + order.plan_id.billing_period
    
    @api.onchange('partner_id')
    def _onchange_timetracker_partner_id(self):
        for sale in self:
            invoice_address_id = False
            if sale.partner_id:
                if sale.partner_id.parent_id:
                    sale.parent_partner_id = sale.partner_id.parent_id.id
                    if sale.partner_id.parent_id.property_inbound_payment_method_line_id:
                        sale.payment_term_id = sale.partner_id.parent_id.property_inbound_payment_method_line_id.id
                    if sale.partner_id.parent_id.child_ids:
                        for child in sale.partner_id.parent_id.child_ids:
                            # if child.type == "invoice":
                            #     sale.partner_invoice_id = child.id
                            sale.partner_invoice_id = sale.partner_id.parent_id.id
                            if child.type == "delivery":
                                sale.partner_shipping_id = child.id
                if sale.partner_id.child_ids:
                    sale.parent_partner_id = sale.partner_id.id
                    for child in sale.partner_id.child_ids:
                        if child.type == "invoice":
                            sale.partner_invoice_id = child.id
                        if child.type == "delivery":
                            sale.partner_shipping_id = child.id


    
    def calculate_distribution(self):
        for order in self:
            logging.warning("calcula distri")
            subtotal_license = 0
            subtotal_transmision = 0
            for line in order.order_line:
                if line.product_id.type_product_service == "license":
                    subtotal_license += line.price_subtotal
                if line.product_id.type_product_service == "transmision":
                    subtotal_transmision += line.price_subtotal

            for line in order.order_line:
                if line.product_id.type_product_service == "transmision":
                    line.distribution = line.price_subtotal * -1
                    line.total_general = line.distribution + line.price_subtotal
                else:
                    if subtotal_license > 0:
                        if line.product_id.type_product_service == False:
                            line.total_general = line.distribution + line.price_subtotal
                            line.distribution = 0
                        else:
                            logging.warning(line.price_subtotal)
                            logging.warning(subtotal_license)
                            logging.warning(subtotal_transmision)
                            line.distribution = (line.price_subtotal / subtotal_license) * subtotal_transmision
                            logging.warning('line.distribution')
                            logging.warning(line.distribution)
                            line.total_general = line.distribution + line.price_subtotal
                    else:
                        line.total_general = line.distribution + line.price_subtotal
    
    def write(self, vals):
        res = super().write(vals)
        logging.warning("write")
        logging.warning(vals)
        self.calculate_distribution()
        return res
    
            
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    periodo = fields.Float('Periodo')
    personal_total_time = fields.Float("Personal total", compute="_compute_personal_total_distribution", store=True)
    distribution = fields.Float("Distribución", compute="_compute_personal_total_distribution", store=True)
    #verificar como eliminar este campo
    #distribucion = fields.Float(string='Distribución', store=True)
    total_general = fields.Float("Total general")
            
    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line()
        if self.periodo > 0:
            res['periodo'] = self.periodo
        return res

    @api.depends('product_uom_qty', 'product_id', 'price_unit', 'discount')
    def _compute_personal_total_distribution(self):
        for line in self:
            logging.warning(line.product_id.name)
            logging.warning(line.subscription_plan_id)
            if line.subscription_plan_id:
                period = line.subscription_plan_id.billing_period_value
                personal_total = 0
                subtotal_license = 0
                distribution = 0
                price_unit_line = line.product_id.list_price
                if line.product_id.type_product_service == "license":
                    personal_total = line.product_uom_qty * line.subscription_plan_id.billing_period_value
                line.personal_total_time = personal_total
                line.periodo = period
                #     for line_sub in line.subscription_plan_id.product_subscription_pricing_ids:
                #         logging.warning(line.product_id.id)
                #         logging.warning(line_sub.product_template_id.id)
                #         if line.product_id.name == line_sub.product_template_id.name:
                #             logging.warning("............")
                #             logging.warning(line_sub.price)
                #             price_unit_line = line_sub.price
                # logging.warning(price_unit_line)
                # line.price_unit = price_unit_line

                # if line.product_id.type_product_service == "license":
                #     personal_total = price_unit_line

                # line.personal_total_time = personal_total
                
                
class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def action_apply_discount(self):
        res = super().action_apply_discount()
        self.sale_order_id.order_line._compute_personal_total_distribution()
        self.sale_order_id.calculate_distribution()
        logging.warning("inherti action_apply_discount")
        return res
                