#Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cu_common')
    def _get_cu_common_template_data(self):
        return {
            'name': _('Cuba - Plan Contable Común'),
            'visible': 0,
            'code_digits': '10',
            'property_account_receivable_id': 'account_common_1350000',
            'property_account_payable_id': 'account_common_4050000',
            'property_account_expense_categ_id': 'account_common_8140000',
            'property_account_income_categ_id': 'account_common_9000000',
        }

    @template('cu_common', 'res.company')
    def _get_cu_common_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cu',
                'bank_account_code_prefix': '109.',
                'cash_account_code_prefix': '101.',
                'transfer_account_code_prefix': '696.',
                'account_default_pos_receivable_account_id': 'account_common_1300020',
                'income_currency_exchange_account_id': 'account_common_9240000',
                'expense_currency_exchange_account_id': 'account_common_8390000',
                'account_journal_suspense_account_id': 'account_common_6990000',
                'account_journal_early_pay_discount_loss_account_id': 'account_common_8350000',
                'account_journal_early_pay_discount_gain_account_id': 'account_common_9200000',
                'default_cash_difference_income_account_id': 'account_common_9240000',
                'default_cash_difference_expense_account_id': 'account_common_8390000',
                'deferred_expense_account_id': 'account_common_3060020',
                'deferred_revenue_account_id': 'account_common_5450000',
                'transfer_account_id': 'account_common_6960000',
            },
        }
