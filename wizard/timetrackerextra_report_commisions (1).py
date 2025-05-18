# -*- encoding: utf-8 -*-

from odoo import models, fields, api
import logging

class ReporteCommisions(models.TransientModel):

    _name = 'timetrackerextra.report_commisions'

    date_from = fields.Date("Fecha desde")
    date_to = fields.Date("Fecha hasta")


    def confirm_action(self):
        invoice_line_list = []
        data_ids = []
        domain = [("id","in",data_ids)]
        payment_ids = self.env["account.payment"].search([("payment_type","=","inbound"),("date",">=",self.date_from),("date","<=", self.date_to),("reconciled_invoice_ids","!=",False)],order="date asc")
        tracker_ids = self.env["timetrackerextra.transient_report_commissions"].search([])
        logging.warning(tracker_ids)
        if tracker_ids:
            tracker_ids.unlink()
        invoices = []
        payment_by_invoice = {}
        if payment_ids:
            for payment in payment_ids:
                for invoice in payment.reconciled_invoice_ids:
                    if invoice.id not in payment_by_invoice:
                        payment_by_invoice[invoice.id] = {'paid_amount': 0, 'invoice_id': invoice, 'firste_date_payment': False}
                        paid_amount = 0
                        for line in invoice.line_ids:
                            matched_entries = line.matched_debit_ids + line.matched_credit_ids
                            for matched in matched_entries:
                                payment_move = matched.debit_move_id.move_id if matched.debit_move_id.move_id.move_type == 'entry' else matched.credit_move_id.move_id
                                payment = self.env['account.payment'].search([('move_id', '=', payment_move.id),('date','!=', False)], limit=1)
                                if payment and payment.date >= self.date_from and payment.date <= self.date_to:
                                    payment_id = payment
                                    paid_amount = matched.amount
                                    logging.warning("payment")
                                    logging.warning(payment)
                                    logging.warning(matched.amount)
                                    payment_by_invoice[invoice.id]['paid_amount'] += matched.amount
                                    if payment_by_invoice[invoice.id]['firste_date_payment'] == False:
                                        payment_by_invoice[invoice.id]['firste_date_payment'] = payment.date

        if len(payment_by_invoice) > 0:
            for invoice in payment_by_invoice:
                for line in payment_by_invoice[invoice]['invoice_id'].invoice_line_ids:
                    #p1
                    sum_subtotal_distribution = line.price_subtotal + line.distribution
                    paid_amount_line = payment_by_invoice[invoice]['paid_amount']
                    amount_total_invoice_line = line.move_id.amount_total
                    #p2
                    paid_percentage_line = (paid_amount_line / amount_total_invoice_line)
                    paid_percentage_line_percent = (paid_amount_line / amount_total_invoice_line) * 100
                    #p1xp2
                    paid_amount_distribution_line = sum_subtotal_distribution * paid_percentage_line
                    product_contact_commission = line.product_id.chain_store.commission_percentaje
                    chain_commission = (paid_amount_distribution_line * product_contact_commission) if product_contact_commission > 0 else 0
                    invoice_user_id = line.move_id.invoice_user_id.id
                    invoice_id = line.move_id.id
                    partner_id = line.move_id.partner_id.id
                    fecha_factura = line.move_id.invoice_date
                    product_id = line.product_id.id
                    type_product = line.product_id.type_product if line.product_id.type_product else "none"
                    chain_store_id = line.product_id.chain_store.id
                    subtotal = line.price_subtotal
                    amount_tax = line.price_total - line.price_subtotal
                    total = line.price_total
                    distributed_paid_amount = paid_amount_distribution_line
                    amount_residual = line.move_id.amount_residual
                    firste_date_payment = payment_by_invoice[invoice]['firste_date_payment']
                    periodo = line.periodo
                    personal_total_time = line.personal_total_time
                    distribution = line.distribution
                    total_general = line.total_general
                    price_unit = line.price_unit
                    move_line_dic = {
                        "invoice_user_id": invoice_user_id,
                        "invoice_id": invoice_id,
                        "partner_id": partner_id,
                        "fecha_factura": fecha_factura,
                        "product_id": product_id,
                        "price_unit": price_unit,
                        "type_product": type_product,
                        "chain_store_id": chain_store_id,
                        "chain_commission": chain_commission,
                        "periodo":periodo,
                        "personal_total_time": personal_total_time,
                        "distribution": distribution,
                        "total_general": total_general,
                        "subtotal": subtotal,
                        "amount_tax": amount_tax,
                        "total": total,
                        "distributed_paid_amount": distributed_paid_amount,
                        "amount_residual": amount_residual,
                        "firste_date_payment": firste_date_payment,
                    }
                    invoice_line_list.append(move_line_dic)

        # if payment_ids:
        #     for payment in payment_ids:
        #         for invoice in payment.reconciled_invoice_ids:
        #             if invoice.id not in invoices:
        #                 invoices.append(invoice.id)
        #                 payment_id = False
        #                 paid_amount = 0
        #                 for line in invoice.line_ids:
        #                     matched_entries = line.matched_debit_ids + line.matched_credit_ids
        #                     for matched in matched_entries:
        #                         payment_move = matched.debit_move_id.move_id if matched.debit_move_id.move_id.move_type == 'entry' else matched.credit_move_id.move_id
        #                         payment = self.env['account.payment'].search([('move_id', '=', payment_move.id),('date','!=', False)], limit=1)
        #                         if payment and payment.date >= self.date_from and payment.date <= self.date_to:
        #                             payment_id = payment
        #                             paid_amount = matched.amount
        #                             logging.warning("payment")
        #                             logging.warning(payment)
        #                             logging.warning(matched.amount)
                        
                        # if invoice.invoice_line_ids:
                        #     for line in invoice.invoice_line_ids:
                        #         #p1
                        #         sum_subtotal_distribution = line.price_subtotal + line.distribution
                        #         paid_amount_line = paid_amount
                        #         amount_total_invoice_line = line.move_id.amount_total
                        #         #p2
                        #         paid_percentage_line = (paid_amount_line / amount_total_invoice_line)
                        #         paid_percentage_line_percent = (paid_amount_line / amount_total_invoice_line) * 100
                        #         #p1xp2
                        #         paid_amount_distribution_line = sum_subtotal_distribution * paid_percentage_line
                        #         product_contact_commission = line.product_id.chain_store.commission_percentaje
                        #         chain_commission = (paid_amount_distribution_line * product_contact_commission) if product_contact_commission > 0 else 0
                        #         invoice_user_id = line.move_id.invoice_user_id.id
                        #         invoice_id = line.move_id.id
                        #         partner_id = line.move_id.partner_id.id
                        #         fecha_factura = line.move_id.invoice_date
                        #         product_id = line.product_id.id
                        #         type_product = line.product_id.type_product if line.product_id.type_product else "none"
                        #         chain_store_id = line.product_id.chain_store.id
                        #         subtotal = line.price_subtotal
                        #         amount_tax = line.price_total - line.price_subtotal
                        #         total = line.price_total
                        #         distributed_paid_amount = paid_amount_distribution_line
                        #         amount_residual = line.move_id.amount_residual
                        #         firste_date_payment = payment_id.date
                                #periodo = line.periodo
                                #personal_total_time = line.personal_total_time
                                #distribution = line.distribution
                                #total_general = line.total_general
                                #price_unit = line.price_unit
                                #move_line_dic = {
                                #    "invoice_user_id": invoice_user_id,
                                #    "invoice_id": invoice_id,
                                #    "partner_id": partner_id,
                                 #   "fecha_factura": fecha_factura,
                                 #   "product_id": product_id,
                                 #   "price_unit": price_unit,
                                 #   "type_product": type_product,
                                 #   "chain_store_id": chain_store_id,
                                 #   "chain_commission": chain_commission,
                                 #   "periodo":periodo,
                                 #   "personal_total_time": personal_total_time,
                                 #   "distribution": distribution,
                                 #   "total_general": total_general,
                                 #   "subtotal": subtotal,
                                 #   "amount_tax": amount_tax,
                                  #  "total": total,
                                 #   "distributed_paid_amount": distributed_paid_amount,
                                   # "amount_residual": amount_residual,
                                    #"firste_date_payment": firste_date_payment,
                                #}        
        if len(invoice_line_list) > 0:
            for line in invoice_line_list:
                logging.warning(line)
                line_tracker_id = self.env["timetrackerextra.transient_report_commissions"].create(line)
                data_ids.append(line_tracker_id.id)
        #view_id = self.env['ir.ui.view'].search([("name","=","view.rtimetrackerextra.transient_report_commissions")])

        return {

            'type': 'ir.actions.act_window',
            #'action': 'time_tracker.record_action_comission',
            'name': 'Comisiones',
            #'view_id': view_id.id,
            #'view_id': 3247,
            'res_model': 'timetrackerextra.transient_report_commissions',
            'view_mode': 'list,pivot',
            'domain': domain,
            'target': 'current'
        } 
