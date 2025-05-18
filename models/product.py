# -*- coding: utf-8 -*-

from odoo import models, fields


class Parner(models.Model):
    _name = 'res.partner'

    color = fields.Integer(string='Color Index', default=0)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type_product = fields.Selection(selection_add=[('certificacion','Certificación'),
                                                   ('formax','Formax'),
                                                   ('equipos_biometricos','Equipos Biométricos'),
                                                   ('prenomina','Prenómina'),
                                                   ('otros','Otros')],ondelete={"certificacion": "cascade","formax": "cascade","equipos_biometricos": "cascade","prenomina": "cascade","otros": "cascade"})
