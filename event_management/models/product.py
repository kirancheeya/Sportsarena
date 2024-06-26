from odoo import models, fields, api


class Product(models.Model):
    _name = 'event_management.product'
    _description = 'Product Information'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    quantity_available = fields.Integer(string='Quantity Available')
    orders = fields.Many2many('event_management.order', string='Orders')
