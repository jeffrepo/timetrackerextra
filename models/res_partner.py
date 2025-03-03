# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('retail', 'Retail'), ('no_retail', 'No retail'), ('agencia', 'Agencia')], string='Tipo de contacto')