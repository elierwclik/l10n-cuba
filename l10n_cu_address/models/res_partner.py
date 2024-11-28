# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    municipality_id = fields.Many2one('res.state.municipality', 'Municipio', help="Municipio de Cuba")
