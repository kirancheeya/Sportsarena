from odoo import models, fields, api


class Supplier(models.Model):
    _name = 'event_management.supplier'
    _description = 'Supplier Information'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    country = fields.Char(string='Country')
    products_supplied = fields.Many2many('event_management.product', string='Products Supplied')
    payment_terms = fields.Selection([('net_30', 'Net 30'), ('net_60', 'Net 60'), ('net_90', 'Net 90')],
                                     string='Payment Terms')
