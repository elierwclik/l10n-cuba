# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    municipality_ids = fields.One2many('res.state.municipality', 'state_id', 'Municipios', help="Municipios de Cuba")
