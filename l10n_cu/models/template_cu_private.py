# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cu_private')
    def _get_es_pymes_template_data(self):
        return {
            'name': _('Cuba - Plan Contable Sector Privado y Cooperativo'),
            'parent': 'cu_common',
            'sequence': 0,
        }

    @template('cu_private', 'res.company')
    def _get_es_pymes_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cu',
            },
        }
