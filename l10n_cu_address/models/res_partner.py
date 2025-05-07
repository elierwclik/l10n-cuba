# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio', domain="[('state_id', '=', state_id)]",
                                          help="Municipios de Cuba")

    @api.model
    def _clean_and_fix_res_municipality_id(self):
        partners = self.env['res.partner'].search([]).filtered(
            lambda p: p.res_municipality_id and p.res_municipality_id.id not in p.state_id.res_municipality_id.ids)
        partners.write({'res_municipality_id': False})

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.res_municipality_id not in self.state_id.res_municipality_id:
            self.res_municipality_id = False
