# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_settlement_type = fields.Boolean(
        string='Allow Settlement',
        default=False,
        help='If checked, users can process this leave as a settlement.'
    )