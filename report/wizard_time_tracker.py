# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import time
import xlsxwriter
import base64
import io
import logging

class TimetrackerextraWizard(models.TransientModel):
    _name = 'timetrackerextra.wizard_time_tracker'

    fecha_desde = fields.Date(string="Fecha Inicial", required=True, default=lambda self: time.strftime('%Y-%m-01'))
    fecha_hasta = fields.Date(string="Fecha Final", required=True, default=lambda self: time.strftime('%Y-%m-%d'))
    cantidad_documentos = fields.Float('Cantidad de documento')

    def aplicar_accion(self):
        for w in self:
            contador = 0
            logging.warning('entrando a accion')
            linea_factura_ids = self.env['account.move.line'].search([('product_id','in',  [1842,2077,2047,1991,2023,1923,1956]),('move_id.invoice_date','>=',w.fecha_desde), ('move_id.invoice_date','<=', w.fecha_hasta) ])
            if linea_factura_ids:
                logging.warning(linea_factura_ids)
                for linea in linea_factura_ids:
                    if linea.move_id.state == "posted":
                        move_id = linea.move_id
                        move_id.button_draft()
                        move_id.write(
                        {'invoice_line_ids': [(3,linea.id)]})
                        # linea.unlink()
                        move_id.action_post()
                        contador += 1
            w.cantidad_documentos = contador
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'timetrackerextra.wizard_time_tracker',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
