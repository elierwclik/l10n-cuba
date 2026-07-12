# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    res_municipality_id = fields.Many2one('res.municipality', 'Municipio', domain="[('state_id', '=', state_id)]",
                                          help="Municipios de Cuba")

    municipality_name = fields.Char(string="Nombre del Municipio", related='res_municipality_id.name')

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.res_municipality_id not in self.state_id.res_municipality_ids:
            self.res_municipality_id = False

    @api.model
    def _address_fields(self):
        return super()._address_fields() + ['municipality_name']

    def _sanitize_municipality_id(self, vals):
        """Sanitize the municipality value based on the selected state.

        Ensures that ``res_municipality_id`` is only kept in ``vals`` when it
        actually belongs to the state referenced by ``state_id``. This
        prevents inconsistent data where a municipality from one state is
        linked to a record with a different (or no) state assigned.

        :param dict vals: values dictionary passed to create/write, expected
            to optionally contain 'res_municipality_id' and 'state_id'.
        :return: the same vals dictionary, with 'res_municipality_id' set to
            None when it does not belong to the given state.
        :rtype: dict
        """
        if 'res_municipality_id' in vals:
            municipality_id = vals['res_municipality_id']
            state_id = self.env['res.country.state'].browse(
                vals.get('state_id')
            ).exists()
            if not state_id or not municipality_id in state_id.res_municipality_id.ids:
                vals['res_municipality_id'] = None
        return vals

    def write(self, vals):
        """Override write to sanitize 'res_municipality_id' before saving.

        :param dict vals: values to write on the record(s).
        :return: True if was successful.
        :rtype: bool
        """
        vals.update(self._sanitize_municipality_id(vals))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to sanitize 'res_municipality_id' for each record.

        :param list[dict] vals_list: list of values dictionaries for the
            records to create.
        :return: the newly created record(s).
        :rtype: recordset
        """
        for vals in vals_list:
            vals.update(self._sanitize_municipality_id(vals))

        return super().create(vals_list)
