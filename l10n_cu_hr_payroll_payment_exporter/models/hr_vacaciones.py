# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime

from odoo import models, fields, api
from odoo.tools.translate import _

from odoo.exceptions import UserError, ValidationError


# Submayor de vacaciones
# Lonna Y Lestapi Dreke 2022
class Vacaciones(models.Model):
    _name = 'hr.vacaciones'
    _description = 'Vacaciones'

    employee_id = fields.Many2one('hr.employee')
    hr_payslip_run_id = fields.Many2one('hr.payslip.run')
    company_id = fields.Many2one('res.company')
    dias_inicial = fields.Float(string='Vacaciones Acumuladas Dias', default=0.00, precision_digits=2)
    importe_inicial = fields.Float(string='Vacaciones Acumuladas Importe', default=0.00, precision_digits=2)
    dias_ganado = fields.Float(string='Vacaciones Acumuladas Dias', default=0.00, precision_digits=2)
    importe_ganado = fields.Float(string='Vacaciones Acumuladas Importe', default=0.00, precision_digits=2)
    dias_pagado = fields.Float(string='Vacaciones Acumuladas Dias', default=0.00, precision_digits=2)
    importe_pagado = fields.Float(string='Vacaciones Acumuladas Importe', default=0.00, precision_digits=2)
    dias_final = fields.Float(string='Vacaciones Acumuladas Dias', default=0.00, precision_digits=2)
    importe_final = fields.Float(string='Vacaciones Acumuladas Importe', default=0.00, precision_digits=2)
    # negativo = fields.Boolean(string='Si es negativo', default=False)
    date_start = fields.Date(string='Fecha de Inicio', default=datetime.now().strftime('%Y-%m-%d'))
    date_end = fields.Date(string='Fecha de Fin', default=datetime.now().strftime('%Y-%m-%d'))
