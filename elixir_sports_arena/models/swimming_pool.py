from odoo import models, fields, api, exceptions


class SwimmingPoolCourt(models.Model):
    _name = 'elixir.swimming_pool_court'
    _description = 'Swimming Pool Court'

    name = fields.Char(string='Pool Name', required=True)
    indoor_price_per_hour = fields.Float(string='Price per Hour',compute='_compute_price_per_hour',store=True )
    Base_capacity = fields.Float(string='Base Capacity', required=True)
    capacity = fields.Float(string='Capacity', required=True)
    pool_type = fields.Selection([('indoor', 'Indoor'), ('outdoor', 'Outdoor')], string='Pool Type')

    @api.depends('pool_type')
    def _compute_price_per_hour(self):
        for pool in self:
            if pool.pool_type == 'indoor':
                pool.indoor_price_per_hour = 250
            else:
                pool.indoor_price_per_hour = 400
