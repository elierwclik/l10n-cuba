# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    total_ps = fields.Float(string='Total')
    total_on_payable = fields.Boolean(string='Not Payable', store=True)

    def refund_sheet(self):
        res = super().refund_sheet()
        self.write({'state': 'cancel'})
        return res

    def action_payslip_done(self):
        res = super().action_payslip_done()
        vacation_rule = self.env.ref(
            'l10n_cu_hr_payroll_enterprise.hr_payroll_rules_09_dias', raise_if_not_found=False
        )
        if not vacation_rule:
            return res
        holiday_status = self.env.ref('hr_holidays.holiday_status_cl', raise_if_not_found=False)
        if not holiday_status:
            return res
        for slip in self:
            for line in slip.line_ids:
                if line.salary_rule_id == vacation_rule and line.total > 0:
                    allocation = self.env['hr.leave.allocation'].create({
                        'name': _('Vacaciones acumuladas %s') % slip.employee_id.name,
                        'number_of_days': line.total,
                        'employee_id': slip.employee_id.id,
                        'holiday_status_id': holiday_status.id,
                    })
                    allocation.action_confirm()
                    allocation.action_validate()
        return res

    def compute_sheet(self):
        res = super().compute_sheet()
        for slip in self:
            net_total = 0.0
            for line in slip.line_ids:
                if line.salary_rule_id.code == 'NET':
                    net_total = line.total
                    break
            slip.total_ps = net_total
            slip.total_on_payable = net_total <= 0.0
        return res


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    _order = 'date_start desc'

    qty_payslip = fields.Integer('Nóminas', compute='_compute_qty_payslip', store=False)
    total = fields.Float(string='Total', store=True)

    def _compute_qty_payslip(self):
        for run in self:
            run.qty_payslip = len(run.slip_ids)

    def calculate_slips_total(self):
        for sheet in self:
            sheet.total = 0.0
            for slip in sheet.slip_ids:
                slip.compute_sheet()
                sheet.total += slip.total_ps or 0.0


class HrPayrollOtherInput(models.Model):
    _name = 'hr.payroll.other.input'
    _description = 'Payroll Other Input'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    input_type_id = fields.Many2one('hr.payslip.input.type', 'Input Type', required=True)
    amount = fields.Float('Amount', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
