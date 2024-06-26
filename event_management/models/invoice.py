from odoo import models, fields, api


class Invoice(models.Model):
    _name = 'event_management.invoice'
    _description = 'Invoice Information'

    name = fields.Char(string='Invoice Number', required=True)
    date = fields.Date(string='Invoice Date')
    order_id = fields.Many2one('event_management.order', string='Order')
    amount_due = fields.Float(string='Amount Due')
    status = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('paid', 'Paid')], string='Status')
    payment_date = fields.Date(string='Payment Date')
    payment_method = fields.Selection([('cash', 'Cash'), ('credit_card', 'Credit Card'), ('upi', 'upi')],
                                      string='Payment Method')
    notes = fields.Text(string='Notes')
