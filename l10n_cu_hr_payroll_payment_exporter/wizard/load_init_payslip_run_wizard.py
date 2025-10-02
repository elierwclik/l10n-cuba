import base64
import io
from datetime import datetime

from odoo import models, fields
from odoo.exceptions import ValidationError
from xlrd import open_workbook


# wizard para el submayor de vacaciones
class LoadInitPayslipRun(models.TransientModel):
    _name = 'load.init.payslip.run.wizard'
    _description = 'Carga inicial'

    file = fields.Binary(attachment=True)
    file_name = fields.Char("File Name")

    def file_excel(self):
        try:
            inputx = io.BytesIO()
            inputx.write(base64.decodestring(self.file))
            book = open_workbook(file_contents=inputx.getvalue())
        except:
            raise ValidationError(
                'El formato del fichero tiene que ser xlsx y tiene que tener los campos predeterminados')

        sheet = book.sheets()[0]
        # vac = self.env['hr.vacaciones'].search([])
        nom = self.env['hr.payslip.run'].search([('state', 'in', ['done', 'close'])])

        if len(nom) > 0:
            raise ValidationError('Ya se inicializaron los datos, hay nominas en estado hecho o cerradas')
        else:
            for i in range(1, sheet.nrows):
                dias = sheet.cell(i, 2).value
                importe = sheet.cell(i, 3).value
                ci = int(sheet.cell(i, 4).value)

                empleados = self.env['hr.employee'].search([('identification_id', '=', str(ci))])

                if empleados:
                    if empleados.vaca_dias_acum_init == 0:
                        empleados.vaca_dias_acum_init = dias
                        empleados.vaca_imp_acum_init = importe
                        empleados.vaca_dias_acum = dias
                        empleados.vaca_imp_acum = importe

                        vals = {
                            'hr_payslip_run_id': 0,
                            'company_id': 1,
                            'dias_inicial': round(empleados.vaca_dias_acum_init, 2),
                            'importe_inicial': round(empleados.vaca_imp_acum_init, 2),
                            'dias_ganado': 0,
                            'importe_ganado': 0,
                            'dias_pagado': 0,
                            'importe_pagado': 0,
                            'dias_final': round(empleados.vaca_dias_acum_init, 2),
                            'importe_final': round(empleados.vaca_imp_acum_init, 2),
                            'date_start': datetime.now(),
                            'date_end': datetime.now(),
                            'create_date': datetime.now(),
                        }

                        self.env['hr.vacaciones'].create(vals)
                    else:
                        empleados.vaca_dias_acum_init = dias
                        empleados.vaca_imp_acum_init = importe
                        empleados.vaca_dias_acum = dias
                        empleados.vaca_imp_acum = importe
                        vacas = self.env['hr.vacaciones'].search([('employee_id', '=', empleados.id)])
                        vacas.write({
                            'dias_inicial': round(empleados.vaca_dias_acum_init, 2),
                            'importe_inicial': round(empleados.vaca_imp_acum_init, 2),
                            'dias_final': round(empleados.vaca_dias_acum_init, 2),
                            'importe_final': round(empleados.vaca_imp_acum_init, 2),
                        })
