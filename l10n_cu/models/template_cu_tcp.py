# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cu_tcp')
    def _get_cu_tcp_template_data(self):
        return {
            'name': _('Cuba - Plan Contable TCP (Trabajadores por Cuenta Propia)'),
            'parent': 'cu_common',
            'sequence': 30,
            'property_account_receivable_id': 'account_tcp_1460000',
            'property_account_payable_id': 'account_tcp_6000000',
            'property_account_expense_categ_id': 'account_tcp_8010000',
        }

    @template('cu_tcp', 'res.company')
    def _get_cu_tcp_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cu',
                'cash_account_code_prefix': '101.',
                'bank_account_code_prefix': '109.',
            },
        }
