# -*- coding: utf-8 -*-

from odoo import api, models, fields


class Municipality(models.Model):
    _name = 'res.state.municipality'
    _description = 'Municipio'
    _order = 'code'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', help='El código del municipio', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', 'State')

    _sql_constraints = [
        ('unique_state_id_code', 'UNIQUE(state_id, code)',
         '¡El código del municipio debe ser único por Estado/Provincia!')
    ]

    @api.onchange('country_id')
    def _onchange_country_id(self):
        self.state_id -= self.state_id.filtered(
            lambda state: state._origin.id not in self.country_id.state_ids.ids
        )
