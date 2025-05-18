# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):

    _inherit = 'account.invoice.report'

    # l10n_ar_state_id = fields.Many2one('res.country.state', 'Delivery Province', readonly=True)
    # date = fields.Date(readonly=True, string="Accounting Date")
    periodo = fields.Float(readonly=True, string="Periodo")
    personal_total_time = fields.Float(readonly=True, string="Personal total")
    distribution = fields.Float(readonly=True, string="Distribucion")
    total_general = fields.Float(readonly=True, string="Total general")
    price_unit = fields.Float(readonly=True, string="Precio unitario")
    chain_store = fields.Many2one('res.partner', readonly=True, string="Cadena comercial")

    _depends = {
        # 'account.move': ['partner_shipping_id', 'date'],
        # 'res.partner': ['state_id'],
        'account.move.line': ['periodo','personal_total_time','distribution','total_general','price_unit'],
        'product.template': ['chain_store']
    }

    def _select(self) -> SQL:
        return SQL("%s, line.periodo, line.personal_total_time, line.distribution, line.total_general, line.price_unit, template.chain_store",
                   super()._select())

    # def _from(self) -> SQL:
    #     return SQL("%s LEFT JOIN res_partner contact_partner ON contact_partner.id = COALESCE(move.partner_shipping_id, move.partner_id)",
    #                super()._from())
