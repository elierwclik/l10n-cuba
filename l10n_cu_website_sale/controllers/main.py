# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class L10nCuWebsiteSale(WebsiteSale):

    def _prepare_address_form_values(self, order_sudo, partner_sudo, address_type, **kwargs):
        rendering_values = super()._prepare_address_form_values(
            order_sudo, partner_sudo, address_type=address_type, **kwargs
        )

        state = request.env['res.country.state'].browse(rendering_values['state_id'])
        ResMunicipality = request.env['res.state.municipality'].sudo()

        rendering_values.update({
            'state': state,
            'municipality': partner_sudo.municipality_id.id,
            'state_municipalities': ResMunicipality.search([('state_id', '=', state.id)]) if state else ResMunicipality,
        })
        return rendering_values

    def _get_mandatory_billing_address_fields(self, country_sudo):
        """ Return the set of mandatory billing field names.

        :param res.country country_sudo: The country to use to build the set of mandatory fields.
        :return: The set of mandatory billing field names.
        :rtype: set
        """
        mandatory_fields = super()._get_mandatory_billing_address_fields(country_sudo)

        if country_sudo.code == 'CU':
            mandatory_fields.add('municipality_id')

        return mandatory_fields

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        """ Return the set of mandatory delivery field names.

        :param res.country country_sudo: The country to use to build the set of mandatory fields.
        :return: The set of mandatory delivery field names.
        :rtype: set
        """
        mandatory_fields = super()._get_mandatory_delivery_address_fields(country_sudo)

        if country_sudo.code == 'CU':
            mandatory_fields.add('municipality_id')
            mandatory_fields.remove('city')
        return mandatory_fields

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="json", auth="public",
                methods=["POST"], website=True)
    def l10n_cu_state_infos(self, state, address_type, **kw):
        """
        @note: In Odoo 18.1 has been changed 'type="json"' to 'type="jsonrpc"'
        """
        municipalities = state.get_website_sale_municipalities(address_type=address_type)

        return {
            'municipalities': [(c.id, c.name, c.code) for c in municipalities],
            'municipality_required': state.country_id.code == 'CU'
        }
