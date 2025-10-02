# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import numpy as np
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


# Lonna Y Lestapi Dreke 2022
class Employee(models.Model):
    _inherit = "hr.employee"

    vaca_dias_acum_init = fields.Float(string='Vacaciones Días Ac. Inicial', default=0.00, readonly=True)
    vaca_imp_acum_init = fields.Float(string='Vacaciones Imp Ac.Inicial', default=0.00, readonly=True)
    vaca_dias_acum = fields.Float(string='Vacaciones Días Ac.', default=0.00, readonly=True)
    vaca_imp_acum = fields.Float(string='Vacaciones Imp Ac.', default=0.00, readonly=True)
    no_expediente = fields.Char(string='No. Expediente')
    feriado = fields.Float(string='Feriado', default=0.00)
    no_sucursal = fields.Char(string='Número de Sucursal', default='247')
    vaca_liquidate = fields.Boolean(string='Liquidar Vacaciones', default=False)
   
    # Obtener los dias para la incidencia de Vacaciones Disfrutadas
    def get_vacaciones_a_disfrutar(self, payslip_id):
        dias = 0
        incidencia = self.env['hr.leave'].search([('employee_id.id', '=', self.id),
                                                             ('holiday_status_id.code', '=', 'VacDesc'),
                                                             ('state', '=', 'validate')])
        nomina = self.env['hr.payslip'].search([('id', '=', payslip_id)])
        for sec in incidencia:
            fechai = sec.date_from.strftime("%m-%Y")
            fecha_nomina = nomina.date_from.strftime("%m-%Y")
            if fechai == fecha_nomina:
                hours += sec.number_of_hours_display
        return hours

    # Obtener el importe de Vacaciones a Disfrutar
    def get_imp_vacaciones_a_disfrutar(self):
        imp = 0
        if self.vaca_imp_acum > 0:
            imp = self.vaca_imp_acum / self.vaca_dias_acum
        return imp

    # Obtener los dias para la incidencia de Vacaciones Simultaneas
    def get_vacaciones_simultaneas(self, payslip_id):
        dias = 0
        incidencia = self.env['hr.leave'].search([('employee_id.id', '=', self.id),
                                                             ('holiday_status_id.code', '=', 'vac_simultaneas'),
                                                             ('state', '=', 'validate')])
        nomina = self.env['hr.payslip'].search([('id', '=', payslip_id)])
        for sec in incidencia:
            fechai = sec.date_from.strftime("%m-%Y")
            fecha_nomina = nomina.date_from.strftime("%m-%Y")
            if fechai == fecha_nomina:
                hours += sec.number_of_hours_display
        return hours

    # Obtener el importe de Vacaciones a Simultaneas
    def get_imp_vacaciones_a_simultaneas(self):
        imp = 0
        if self.vaca_imp_acum > 0:
            imp = self.vaca_imp_acum / self.vaca_dias_acum
        return imp