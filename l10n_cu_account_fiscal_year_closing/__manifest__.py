# -*- coding: utf-8 -*-
{   
    'name': 'Cuba- Cierre contable',
    'version': '15.0',
    'summary': """ Plantilla para cierre contable """,
    'author': 'Comunidad Cubana de Odoo',
    'website': '',
    'category': 'Accounting',
    'depends': [
        'base',
        'l10n_cu',
        'account',
        'account_fiscal_year_closing'
    ],
    'data': [
        "data/account_fiscal_year_closing_data.xml"
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
