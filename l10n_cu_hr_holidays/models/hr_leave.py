# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    is_settlement = fields.Boolean(string='Es liquidación', default=False)
    settlement_days = fields.Float(string='Días a liquidar', digits=(16, 2))
    
    is_settlement_enabled = fields.Boolean(related='holiday_status_id.is_settlement_type')

    @api.onchange('is_settlement')
    def _onchange_is_settlement(self):
        if self.is_settlement and self.employee_id:
            # 1. Search for validated holiday allocations
            allocations = self.env['hr.leave.allocation'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', 'validate'),
                ('holiday_status_id.name', 'ilike', self.holiday_status_id.name)  # Ensure it's the same leave type
            ])

            # 2. Sum Net Balance (Assigned - Taken)
            # Use 'number_of_days' or 'max_leaves' depending on your Odoo version
            total_assigned = sum(allocations.mapped('number_of_days'))
            total_taken = sum(allocations.mapped('leaves_taken'))
            
            self.settlement_days = total_assigned - total_taken
        else:
            self.settlement_days = 0.0
    
    @api.onchange('holiday_status_id')
    def _onchange_holiday_status_id_reset(self):
        # Si el nuevo tipo no permite liquidación, desactivamos el check
        if not self.is_settlement_enabled:
            self.is_settlement = False