# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_cliente = fields.Selection([
        ('agencia', 'Agencia'),
        ('distribuidor', 'Distribuidor'),
        ('proveedor', 'Proveedor retail'),
        ('no_proveedor', 'Proveedor no retail'),
        ('cadena', 'Cadena'),
        ('pagador', 'Pagador'),
        ('otros', 'Otros')
    ], string='Tipo de cliente', store=True)
    user_has_group_timetracker_payment = fields.Boolean(compute='_compute_user_has_group_timetracker_payment')
    commission_percentaje = fields.Float("Comisión")
    is_chain = fields.Boolean(string='Is a Chain Store', default=False,
        help="Check if the contact is a company, otherwise it is a person")
    chain_store = fields.Many2one("res.partner", string="Cadena comercial")

    # @api.constrains('tipo_cliente')
    # def _check_tipo_cliente(self):
    #     for cliente in self:
    #         if not cliente.tipo_cliente:
    #             raise ValidationError('Debe seleccionar un tipo de cliente.')

    @api.depends_context('uid')
    def _compute_user_has_group_timetracker_payment(self):
        logging.warning("user_has_group_timetracker_payment")
        user_has_group_timetracker_payment = self.env.user.has_group('timetrackerextra.group_timetracker_forma_pago')
        logging.warning(user_has_group_timetracker_payment)
        for partner in self:
            partner.user_has_group_timetracker_payment = user_has_group_timetracker_payment

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
    #     if self.partner_id and not self.partner_id.tipo_cliente:
    #         raise ValidationError('El cliente seleccionado debe tener un tipo de cliente asignado')