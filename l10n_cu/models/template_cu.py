# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cu')
    def _get_cu_template_data(self):
        return {
            'code_digits': '3',
            'property_account_receivable_id': 'account_common_173',
            'property_account_payable_id': 'account_common_400',
            'property_account_expense_categ_id': 'account_common_835',
            'property_account_income_categ_id': 'account_common_900',

        }

    @template('cu', 'res.company')
    def _get_cu_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cu',
                'bank_account_code_prefix': '102',
                'cash_account_code_prefix': '101',
                'transfer_account_code_prefix': '699',
                'account_default_pos_receivable_account_id': '106.03',
                'income_currency_exchange_account_id': '106',
                'expense_currency_exchange_account_id': '107',
                'deferred_expense_account_id': 'cuenta173_01',
                'account_journal_early_pay_discount_loss_account_id': 'cuenta9993',
                'account_journal_early_pay_discount_gain_account_id': 'cuenta9994',
                'tax_cash_basis_journal_id': 'cbcu',
                'account_sale_tax_id': 'tax12',
                'account_purchase_tax_id': 'tax14',
                'account_cash_basis_base_account_id': 'cuenta801_01_99',
            },
        }

    @template('cu', 'account.journal')
    def _get_cu_account_journal(self):
        return {
            'sale': {
                "name": _("Customer Invoices"),
                "code": "0001",
                #"l10n_latam_use_documents": True,
                "refund_sequence": False,
            },
            'purchase': {
                "name": _("Vendor Bills"),
                "code": "0002",
                #"l10n_latam_use_documents": True,
                "refund_sequence": False,
            },
        }