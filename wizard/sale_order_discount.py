# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import Command, _, api, fields, models


class SaleOrderDiscount(models.TransientModel):
    _inherit = 'sale.order.discount'

    timetracker_discount_type = fields.Selection(
        selection=[
            ('sol_discount', "En todas las líneas de la orden"),
        ],
        default='sol_discount',
    )