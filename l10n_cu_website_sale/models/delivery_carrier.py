from odoo import api, fields, models, _, Command


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    res_municipality_ids = fields.Many2many(
        'res.municipality',
        'delivery_carrier_municipality_rel',
        'carrier_id',
        'res_municipality_id',
        'Municipalities'
    )

    @api.onchange('state_ids')
    def _onchange_state_ids(self):
        self.res_municipality_ids -= self.res_municipality_ids.filtered(
            lambda state: state._origin.id not in self.state_ids.res_municipality_ids.ids
        )

    def _match_address(self, partner):
        match = super(DeliveryCarrier, self)._match_address(partner)
        if self.res_municipality_ids and partner.res_municipality_id not in self.res_municipality_ids:
            return False
        return match
