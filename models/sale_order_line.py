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
    ejecutivo = fields.Boolean("Ejecutivo")
    coordinador = fields.Boolean("Coordinador")
    director_comercial = fields.Boolean("Director comercial")
    director_general = fields.Boolean("Director general")
    # aprobado_por = fields.Many2one("res.users","Aprobador por", compute = "_compute_descuento",store = True, copy = False)
    # fecha_aprobacion = fields.Date("Fecha de aprobación", compute = "_compute_descuento",store = True, copy = False)
    # descuento = fields.Float("Descuento (%)", compute = "_compute_descuento",store = True,  copy = False)
    puesto_autorizador_id = fields.Many2one('hr.job','Puesto autorizador')

    # @api.depends('order_line')
    # def _compute_descuento(self):
    #     for orden in self:
    #         descuento = 0
    #         logging.warning(orden.amount_undiscounted)
    #         logging.warning(orden.amount_untaxed)
    #         monto_descuento = 0
    #         if orden.order_line:
    #             if orden.amount_undiscounted != orden.amount_untaxed:
    #                 monto_descuento = orden.amount_undiscounted - orden.amount_untaxed
    #                 descuento = ((monto_descuento / orden.amount_undiscounted) * 100) if monto_descuento > 0 else 0
    #                 logging.warning("descuento")
    #                 logging.warning(descuento)
    #
    #                 orden.descuento = descuento
    #             else:
    #                 descuento = 0
    #                 orden.descuento = 0
    #                 orden.aprobado_por = False
    #                 orden.fecha_aprobacion = False
    #             logging.warning(self.env.user.employee_id)
    #             if self.env.user.employee_id and self.env.user.employee_id.job_id:
    #                 politica_descuento_id = self.env['timetrackerextra.politica_descuento'].search([('puesto_trabajo_aprobador_id','=',self.env.user.employee_id.job_id.id)])
    #                 logging.warning(politica_descuento_id)
    #                 if politica_descuento_id:
    #                     if politica_descuento_id.tipo_politica == 'sin_limite':
    #                         if descuento <= politica_descuento_id.porcentaje_maximo_descuento:
    #                             orden.aprobado_por = self.env.user.id
    #                             orden.fecha_aprobacion = fields.Datetime.now()
    #                         else:
    #                             orden.aprobado_por = False
    #                             orden.fecha_aprobacion = False
    #                     else:
    #                         logging.warning('monto_descuento')
    #                         if descuento <= politica_descuento_id.porcentaje_maximo_descuento and monto_descuento <= politica_descuento_id.monto_maximo:
    #                             orden.aprobado_por = self.env.user.id
    #                             orden.fecha_aprobacion = fields.Datetime.now()
    #                         else:
    #                             orden.aprobado_por = False
    #                             orden.fecha_aprobacion = False
    #                             puesto_autorizador_id = self.env['timetrackerextra.politica_descuento'].sudo().search([('monto_maximo','>=',monto_descuento),('porcentaje_maximo_descuento','>=',descuento)], order='monto_maximo asc')
    #                             logging.warning(monto_descuento)
    #                             logging.warning(descuento)
    #                             logging.warning('puesto_autorizador_id')
    #                             logging.warning(puesto_autorizador_id)
    #                             if puesto_autorizador_id:
    #                                 orden.puesto_autorizador_id = puesto_autorizador_id.puesto_trabajo_aprobador_id.id
    #
    #
    # def aprobar_descuento(self):
    #     for orden in self:
    #         descuento = 0
    #         logging.warning(orden.amount_undiscounted)
    #         logging.warning(orden.amount_untaxed)
    #         monto_descuento = 0
    #         if orden.amount_undiscounted != orden.amount_untaxed:
    #             monto_descuento = orden.amount_undiscounted - orden.amount_untaxed
    #             descuento = ((monto_descuento / orden.amount_undiscounted) * 100) if monto_descuento > 0 else 0
    #             logging.warning("descuento")
    #             logging.warning(descuento)
    #
    #             #orden.descuento = descuento
    #         logging.warning(self.env.user.employee_id)
    #         if self.env.user.employee_id and self.env.user.employee_id.job_id:
    #             politica_descuento_id = self.env['timetrackerextra.politica_descuento'].search([('puesto_trabajo_aprobador_id','=',self.env.user.employee_id.job_id.id)])
    #             logging.warning(politica_descuento_id)
    #             if politica_descuento_id:
    #                 if politica_descuento_id.tipo_politica == 'sin_limite':
    #                     if round(descuento,2) <= politica_descuento_id.porcentaje_maximo_descuento:
    #                         orden.aprobado_por = self.env.user.id
    #                         orden.fecha_aprobacion = fields.Datetime.now()
    #                     else:
    #                         orden.aprobado_por = False
    #                         orden.fecha_aprobacion = False
    #                         raise UserError(_("La orden debe ser autorizada por los grupos autorizadores"))
    #                 else:
    #                     logging.warning("DESCUENTO")
    #                     logging.warning(descuento)
    #                     logging.warning(politica_descuento_id.porcentaje_maximo_descuento)
    #                     logging.warning(monto_descuento)
    #                     logging.warning(politica_descuento_id.monto_maximo)
    #                     if round(descuento,2) <= politica_descuento_id.porcentaje_maximo_descuento and monto_descuento <= politica_descuento_id.monto_maximo:
    #                         orden.aprobado_por = self.env.user.id
    #                         orden.fecha_aprobacion = fields.Datetime.now()
    #                     else:
    #                         orden.aprobado_por = False
    #                         orden.fecha_aprobacion = False
    #                         puesto_autorizador_id = self.env['timetrackerextra.politica_descuento'].search([('monto_maximo','>=',monto_descuento),('porcentaje_maximo_descuento','<=',descuento)], order='monto_maximo asc')
    #                         logging.warning('puesto_autorizador_id')
    #                         logging.warning(puesto_autorizador_id)
    #                         raise UserError(_("La orden debe ser autorizada por los grupos autorizadores"))
    #             else:
    #                 raise UserError(_("No tiene política de descuento asignada"))
    #     return True

    # def _ordenes_por_aprobar(self):
    #     usuario_puesto_trabajo = {}
    #     empleado_ids = self.env['hr.employee'].search([])
    #     plantilla = self.env.ref('timetrackerextra.mail_template_timetracker_ordenes_autorizar')
    #     logging.warning("plantilla")
    #     logging.warning(plantilla)
    #     if empleado_ids:
    #         for empleado in empleado_ids:
    #             if empleado.job_id and empleado.user_id:
    #                 if empleado.job_id.id not in usuario_puesto_trabajo:
    #                     usuario_puesto_trabajo[empleado.job_id.id] = {'puesto': empleado.job_id.name, 'correos': False, 'ordenes': [] }
    #                 usuario_puesto_trabajo[empleado.job_id.id]['correos'] = empleado.user_id.partner_id.email
    #
    #     orden_ids = self.env['sale.order'].search([('descuento','>', 0),('puesto_autorizador_id','!=', False)])
    #     if orden_ids:
    #         for orden in orden_ids:
    #             puesto_autorizador = orden.puesto_autorizador_id.id
    #             usuario_puesto_trabajo[puesto_autorizador]['ordenes'].append(orden.name)
    #
    #
    #     if usuario_puesto_trabajo:
    #         for puesto in usuario_puesto_trabajo:
    #             logging.warning('puesto')
    #             logging.warning(puesto)
    #             logging.warning(usuario_puesto_trabajo[puesto]['ordenes'])
    #             if len(usuario_puesto_trabajo[puesto]['ordenes']) > 0:
    #                 usuarios = usuario_puesto_trabajo[puesto]['correos']
    #                 valores_correo = {'ordenes': usuario_puesto_trabajo[puesto]['ordenes']}
    #                 ctx = {
    #                     'ordenes': valores_correo['ordenes']
    #                 }
    #                 template = plantilla.with_context(valores_correo).copy()
    #                 template.email_to = usuarios  # set dynamically
    #                 logging.warning(ctx)
    #                 template.with_context(ctx).send_mail(self.id, force_send=True)

    # def autorizar_ejecutivo(self):
    #     for venta in self:
    #         venta.ejecutivo = True
    #     return True
    #
    # def autorizar_coordinador(self):
    #     for venta in self:
    #         venta.coordinador = True
    #     return True
    #
    # def autorizar_director_comercial(self):
    #     for venta in self:
    #         venta.director_comercial = True
    #     return True
    #
    # def autorizar_director_general(self):
    #     for venta in self:
    #         venta.director_general = True
    #     return True

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


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    def action_apply_discount(self):
        res = super().action_apply_discount()
        self.sale_order_id.order_line._compute_personal_total_distribution()
        self.sale_order_id.calculate_distribution()
        #self.sale_order_id._compute_descuento()
        logging.warning("inherti action_apply_discount")
        return res
