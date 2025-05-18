from odoo import models, fields

class TimeTrackerExtraReportCommisions(models.TransientModel):
    _name = 'timetrackerextra.transient_report_commissions'
    
    invoice_user_id = fields.Many2one("res.users", string="Comercial")
    invoice_id = fields.Many2one("account.move", string="Factura")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    fecha_factura = fields.Date("Fecha de factura")
    product_id = fields.Many2one("product.product","Producto")
    price_unit = fields.Float('Precio unitario')
    type_product = fields.Selection([('none', 'No definido'),
                                     ('monitor', 'Monitor'),
                                     ('rpe', 'RPE'),
                                     ('suscription','Suscripción'),
                                     ('certificacion','Certificación'),
                                     ('formax','Formax'),
                                     ('equipos_biometricos','Equipos Biométricos'),
                                     ('prenomina','Prenómina'),
                                     ('otros','Otros')], 'Tipo de producto', default='none', required=True)
    chain_store_id = fields.Many2one('res.partner', string='Cadena comercial')
    chain_commission = fields.Float("Comisión cadena")
    subtotal = fields.Float("Subtotal")
    amount_tax = fields.Float("Impuestos")
    total = fields.Float("Total")
    distributed_paid_amount = fields.Float("Importe pagado distribuido")
    amount_residual = fields.Float("Importe adeudado")
    firste_date_payment = fields.Date("Fecha del primer pago")
    #new fields
    periodo = fields.Float(string="Periodo")
    personal_total_time = fields.Float(string="Personal total")
    distribution = fields.Float(string="Distribución")
    total_general = fields.Float(string="Total general")
    
    
    