# -*- coding: utf-8 -*-
# Part of Idola Odoo Team, Comunidad cubana de Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>


{
    'name': 'Topónimos Cubanos',
    'version': '1.0',
    'author': 'Idola Odoo Team, Comunidad cubana de Odoo',
    'category': 'Localizations',
    'depends': ['base', 'contacts'],
    'countries': ['cu'],
    'data': [
        'data/res_country_state_data.xml',
        'data/res_municipality_data.xml',
        'views/res_municipality_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
    ],
    'auto_install': ['contacts'],
    'license': 'LGPL-3',
}
