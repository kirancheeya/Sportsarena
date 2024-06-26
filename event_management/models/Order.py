from odoo import models, fields, api


class Order(models.Model):
    _name = 'event_management.order'
    _description = 'Order Information'

    name = fields.Char(string='Order Name', required=True)
    date = fields.Date(string='Order Date')
    customer_id = fields.Many2one('event_management.customer', string='Customer')
    products = fields.Many2many('event_management.product', string='Products')
    total_amount = fields.Float(string='Total Amount')
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered')],
                              string='Status')
    payment_method = fields.Selection([('cash', 'Cash'), ('credit_card', 'Credit Card'), ('paypal', 'Paypal')],
                                      string='Payment Method')
    delivery_address = fields.Many2one('event_management.address', string='Delivery Address')
    billing_address = fields.Text(string='Billing Address')
    state = fields.Selection([('draft', 'Draft'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')], default='draft')

    def move_approved(self):
        self.state = 'approved'
