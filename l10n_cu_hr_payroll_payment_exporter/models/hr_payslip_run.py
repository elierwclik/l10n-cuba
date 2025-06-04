# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
# from datetime import datetime
import datetime
import os

import dbf
from odoo import models, fields, api
from odoo.tools.translate import _


class PayslipsRun(models.Model):
    _inherit = 'hr.payslip.run'
    _rec_name = 'no_payslip'

    # Se agrega campo autogenerado
    no_payslip = fields.Char(string='No de nómina', required=True, copy=True, readonly=True, index=True,
                             default=lambda self: _('New'))
    file = fields.Binary('nomina.dbf', attachment=False)
    file_name = fields.Char("File Name")
    est_payslip = fields.Char(string='Prefix de Estructura Salarial', required=False)

    # Se redefine método para generar número de Nómina
    @api.model
    def create(self, vals):
        if vals.get('no_payslip', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('hr.payslip.run') or 'New'
            if 'date_start' in vals:
                month = vals['date_start'][5:7]
                sequence = sequence[:9] + month + sequence[11:]
            vals['no_payslip'] = sequence
        result = super(PayslipsRun, self).create(vals)
        return result

    # devuelve el valor del cualquier linea del splip pasandole el code, el id del splip y el id del empleado
    def valor_slip(self, code, slip_id, emp_id):
        query = """
                    SELECT pl.code, pl.amount
                          	FROM public.hr_payslip_line pl                  	
                          	inner join public.hr_employee emp on emp.id = pl.employee_id
                          	inner join public.hr_payslip ps on ps.id = pl.slip_id
                          	WHERE pl.slip_id = %s AND pl.employee_id = %s
               """
        self._cr.execute(query, (slip_id, emp_id,))

        slip = self._cr.fetchall()

        amount = 0
        for sec in code:
            for items in slip:
                if items[0] == sec:
                    amount += items[1]
        return amount

    # Inserta el numero de la orden en estado 'Done' en el campo no_payslip de la tabla project.task, calcular el total y calcular el submayor
    def done_payslip_run(self):
        res = super(PayslipsRun, self).done_payslip_run()

        self.calculate_submayor()
        return res


    # inserta los datos relacionados con el submayor de vacaciones
    # Lonna Y Lestapi Dreke 2022
    def calculate_submayor(self):
        # def calculate_slips_total(self):
        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', self.id)])

        for items in payslips:
            payslips_line = self.env['hr.payslip.line'].search([('slip_id', '=', items.id),
                                                                ('name', 'ilike', 'VAC')])

            acd = items.employee_id.vaca_dias_acum
            aci = items.employee_id.vaca_imp_acum

            # Recorre la cantidad de tipos de reglas relacionadas con las vacaciones, con el objetivo de formar los pares de dias e importe
            # Hay que adicionar cada par segun la regla relacionada con las vacaciones, las reglas se relacionan por su codigo
            for keys in range(1, 9):
                vac_dias = 0
                vac_imp = 0
                negativo = False
                di = acd
                ii = aci
                for sec in payslips_line:
                    if keys == 1:
                        if 'PVD' == sec.code or 'PVDFijo' == sec.code:
                            vac_dias = sec.amount
                        if 'PROVISIONES_VACACIONES' == sec.code or 'PROVISIONES_VACACIONES1T' == sec.code or 'PROVISIONES_VACACIONES_NO_ASIGNADO' == sec.code or 'PROVISIONES_VACACIONES1NAFijo' == sec.code or 'PROVISIONES_VACACIONESPTT' == sec.code or 'PROVISIONES_VACACIONESPHR' == sec.code or 'PROVISIONES_VACACIONES-FERD' == sec.code or 'PROVISIONES_VACACIONES1NA' == sec.code:
                            vac_imp += sec.amount
                        negativo = False
                    if keys == 2:
                        if 'PVDS' == sec.code:
                            vac_dias = sec.amount
                        if 'PROVISIONES_VACACIONES_SUELDISTA' == sec.code:
                            vac_imp = sec.amount
                        negativo = False
                    if keys == 3:
                        if 'PVDI' == sec.code:
                            vac_dias = sec.amount
                        if 'PROVISIONES_VACACIONES1' == sec.code or 'PROVISIONES_VACACIONES1TT' == sec.code:
                            vac_imp += sec.amount
                        negativo = False
                    if keys == 4:
                        if 'VacDescD' == sec.code:
                            vac_dias = sec.amount
                        if 'VacDescI' == sec.code:
                            vac_imp = sec.amount
                        negativo = True
                    if keys == 5:
                        if 'VacDescDS' == sec.code:
                            vac_dias = sec.amount
                        if 'VacDescIS' == sec.code:
                            vac_imp = sec.amount
                        negativo = True
                    if keys == 6:
                        if 'VacDescDI' == sec.code:
                            vac_dias = sec.amount
                        if 'VacDescII' == sec.code:
                            vac_imp = sec.amount
                        negativo = True
                    if keys == 7:
                        if 'vac_simultaneasD' == sec.code:
                            vac_dias = sec.amount
                        if 'vac_simultaneasI' == sec.code:
                            vac_imp = sec.amount
                        negativo = True
                    if keys == 8:
                        if 'LVD' == sec.code:
                            vac_dias = sec.amount
                        if 'LV' == sec.code:
                            vac_imp = sec.amount
                        negativo = True

                if vac_dias > 0 and vac_imp > 0:
                    sd = round(vac_dias, 2)
                    si = round(vac_imp, 2)
                    if negativo:
                        acd -= sd
                        aci -= si
                        pagagod = sd
                        pagadoi = si
                        sd = 0
                        si = 0
                    else:
                        acd += sd
                        aci += si
                        pagagod = 0
                        pagadoi = 0
                    vals = {
                        'employee_id': items.employee_id.id,
                        'hr_payslip_run_id': self.id,
                        'company_id': items.company_id.id,
                        'dias_inicial': round(di, 2),
                        'importe_inicial': round(ii, 2),
                        'dias_ganado': round(sd, 2),
                        'importe_ganado': round(si, 2),
                        'dias_pagado': '-' + str(round(pagagod, 2)),
                        'importe_pagado': '-' + str(round(pagadoi, 2)),
                        'dias_final': round(acd, 2),
                        'importe_final': round(aci, 2),
                        'date_start': self.date_start,
                        'date_end': self.date_end,
                        'create_date': datetime.datetime.now(),
                    }

                    self.env['hr.vacaciones'].create(vals)
                    self.env['hr.employee'].search([('id', '=', items.employee_id.id)]).update(
                        {'vaca_dias_acum': acd, 'vaca_imp_acum': aci})

        self.calculo_acumulados_vac(payslips)

    # calcula y actualiza en cada trabajador su acumulado de vacaciones en dias y en importe
    def calculo_acumulados_vac(self, obj_payslip):

        for sec in obj_payslip:

            payslips_vac = self.env['hr.vacaciones'].search([('employee_id.id', '=', sec.employee_id.id),
                                                             ('hr_payslip_run_id.id', '=', self.id)])

            for items in payslips_vac:
                sec.vac_acum_dias = items.dias_final
                sec.vac_acum_imp = items.importe_final
  

    # Construye el fichero dbf segun la nomina
    def dbf_file(self):
        dict_slip = {}
        cont = 0
        dicNew = {}
        list = []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir = str(BASE_DIR).replace("\\", "/") + '/data/nomina.dbf'

        table = dbf.Table(dir,
                          'NUM_IDEPER C(11); CTA_MNAC C(16); CTA_MLC C(16); IMPORTE_N N(16,2); IMPORTE_D N(16,2); COD_PAEXID C(3); COD_TIPID C(2)')

        table.open(mode=dbf.READ_WRITE)

        nomina = self.env['hr.payslip.run'].search([('date_start', '>=', self.date_start),
                                                    ('date_end', '<=', self.date_end),
                                                    ('state', '=', 'done')])

        payslips = self.env['hr.payslip'].search([('payslip_run_id', 'in', [items.id for items in nomina]),
                                                  ('state', '!=', 'cancel')])
        SN = 0.00
        for sec in payslips:

            if sec.employee_id.bank_account_id.acc_number is not False:

                for items in self.env['hr.payslip.line'].search([('slip_id', '=', sec.id)]):
                    if items.code == 'NETDC':
                        SN += items.amount
                    if items.code == 'NETC':
                        SN += items.amount
                    if items.code == 'NTSCC':
                        SN += items.amount

                vals = {
                    'ci': sec.employee_id.identification_id if sec.employee_id.identification_id is not False else '',
                    'no_account': sec.employee_id.bank_account_id.acc_number if sec.employee_id.bank_account_id.acc_number is not False else '',
                    'import': SN if SN is not False else 0.00,
                    'sucursal': sec.employee_id.no_sucursal if sec.employee_id.no_sucursal is not False else ''
                }
                dict_slip[cont] = vals
                cont += 1

        def exist(val, dict):
            for key in dict:
                if dict[key]['ci'] == val['ci']:
                    dict[key]['import'] += val['import']

        for key, val in dict_slip.items():
            if val['ci'] not in list:
                list.append(val['ci'])
                dicNew[key] = dict_slip[key]
            else:
                exist(val, dicNew)

        for key, val in dicNew.items():
            table.append((val['ci'],
                          val['no_account'],
                          '',
                          val['import'],
                          None, val['sucursal'], 'CI'))

        with open(dir, 'rb') as files:
            self.file_name = 'nomina.dbf'
            self.file = base64.b64encode(files.read())
            files.close()
