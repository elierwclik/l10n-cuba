# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class L10nCuWebsiteSale(CustomerPortal):

    def _prepare_address_form_values(
            self,
            *args,
            callback='',
            order_sudo=False,
            **kwargs
    ):
        rendering_values = super()._prepare_address_form_values(
            *args, callback=callback, order_sudo=order_sudo, **kwargs
        )
        current_partner_id = rendering_values['current_partner']
        state = request.env['res.country.state'].browse(
            rendering_values['state_id']
        )
        ResMunicipality = request.env['res.municipality'].sudo()

        rendering_values.update({
            'state': state,
            'res_municipality_id': current_partner_id.res_municipality_id.id,
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
            mandatory_fields.add('res_municipality_id')

        return mandatory_fields

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        """ Return the set of mandatory delivery field names.

        :param res.country country_sudo: The country to use to build the set of mandatory fields.
        :return: The set of mandatory delivery field names.
        :rtype: set
        """
        mandatory_fields = super()._get_mandatory_delivery_address_fields(country_sudo)

        if country_sudo.code == 'CU':
            mandatory_fields.add('res_municipality_id')
            mandatory_fields.remove('city')
        return mandatory_fields

    @http.route(
        ['/l10n_cu/state_infos/<model("res.country.state"):state>'],
        type="jsonrpc",
        auth="public",
        methods=["POST"],
        website=True
    )
    def l10n_cu_state_infos(self, state, address_type, **kw):
        """
        Return state municipalities and municipality requirement flag.

        :rtype: dict
        """
        return {
            'municipalities': [(c.id, c.name, c.code) for c in state.sudo().res_municipality_ids],
            'municipality_required': state.country_id.code == 'CU'
        }
