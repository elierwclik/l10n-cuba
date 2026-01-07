from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResCountry(models.Model):
    _inherit = 'res.country'

    city_required = fields.Boolean(default=True, string='City Required')
    municipality_required = fields.Boolean(default=False, string='Municipality Required')
