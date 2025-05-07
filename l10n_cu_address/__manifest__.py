# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>


{
    "name" : "Topónimos Cubanos",
    "version" : "17.0.2.0.1",
    "author" : "Idola Odoo Team, Comunidad cubana de Odoo",
    "category": "Localization",
    "depends" : [
        'base',
        'contacts'
    ],
    "license": "AGPL-3",
    "data" : [
        'data/res_country_state_data.xml',
        'data/res_municipality_data.xml',
        'views/res_municipality_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',

        # fix's
        'data/res_municipalities_fix.xml'
    ],
    "auto_install": True,

}
