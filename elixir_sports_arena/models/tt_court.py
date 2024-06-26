from odoo import models, fields, api, exceptions


class TTCourt(models.Model):
    _name = 'elixir.tt_court'
    _description = 'Table Tennis Court'

    name = fields.Char(string='Court Name', required=True)
    indoor_price_per_hour = fields.Float(string=' Price per Hour', compute='_compute_price_per_hour', store=True)
    # outdoor_price_per_hour = fields.Float(string='Outdoor Price per Hour', required=True)
    court_type = fields.Selection([('indoor', 'Indoor'), ('outdoor', 'Outdoor')], string='Court Type')

    @api.depends('court_type')
    def _compute_price_per_hour(self):
        for courts in self:
            if courts.court_type == 'indoor':
                courts.indoor_price_per_hour = 250
            else:
                courts.indoor_price_per_hour = 400
