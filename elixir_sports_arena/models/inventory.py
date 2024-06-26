from odoo import models, fields

class SportsInventory(models.Model):
    _name = 'sports.inventory'
    _description = 'Sports Arena Inventory'

    item_type = fields.Selection([
        ('racket', 'Racket'),
        ('shuttle', 'Shuttle')
    ], string='Item Type', required=True)
    name = fields.Char(string='Racket Name')
    original_price = fields.Float(string='Original Price', required=True)
    rental_price = fields.Float(string='Rental Price', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    description = fields.Text(string='Description')
    booking_id = fields.Many2one('elixir.booking', string='Booking')


    # Add any other fields as needed

    _sql_constraints = [
        ('positive_original_price', 'CHECK(original_price > 0)', 'Original price must be positive.'),
        ('positive_rental_price', 'CHECK(rental_price > 0)', 'Rental price must be positive.')
    ]