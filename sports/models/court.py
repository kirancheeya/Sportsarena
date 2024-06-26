from odoo import models, fields, api


class BadmintonCourt(models.Model):
    _name = 'sports.badminton_court'
    _description = 'Badminton Court'

    name = fields.Char('Court Name', required=True)
    court_type = fields.Selection([
        ('synthetic', 'Synthetic'),
        ('wooden', 'Wooden')
    ], string='Court Type', required=True)
    price_per_hour = fields.Float('Price per Hour', compute='_compute_price_per_hour')
    capacity = fields.Integer('Capacity', default=2)

    @api.depends('court_type')
    def _compute_price_per_hour(self):
        for court in self:
            if court.court_type == 'synthetic':
                court.price_per_hour = 250
            elif court.court_type == 'wooden':
                court.price_per_hour = 150
            else:
                court.price_per_hour = 0

