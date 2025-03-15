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