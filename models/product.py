# -*- coding: utf-8 -*-

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # type_product = fields.Selection(selection_add=[('certificacion','Certificación'),
    #                                                ('formax','Formax'),
    #                                                ('equipos_biometricos','Equipos Biométricos'),
    #                                                ('prenomina','Prenómina'),
    #                                                ('otros','Otros')],ondelete={"certificacion": "cascade","formax": "cascade","equipos_biometricos": "cascade","prenomina": "cascade","otros": "cascade"})
    type_product_service = fields.Selection([('transmision', 'Transmision'), ('license', 'Licencia')], string='Tipo de servicio')
    type_product = fields.Selection([('none', 'No definido'),
                                     ('monitor', 'Monitor'),
                                     ('rpe', 'RPE'),
                                     ('suscription','Suscripción'),
                                     ('certificacion','Certificación'),
                                     ('formax','Formax'),
                                     ('equipos_biometricos','Equipos Biométricos'),
                                     ('prenomina','Prenómina'),
                                     ('otros','Otros')], 'Type of product', default='none', required=True)
    chain_store = fields.Many2one('res.partner', string='Cadena comercial', domain="[('is_company','=',True),('tipo_cliente', '=', 'cadena')]")