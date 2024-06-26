from odoo import models, fields, api


class CancellationDetails(models.Model):
    _name = 'elixir.cancellation.details'
    _description = 'Cancellation Details'

    booking_no = fields.Char(string='Booking No')
    customer_id = fields.Many2one('elixir.customer', string='Customer')
    employee_id = fields.Many2one('elixir.employee', string='Employee')
    reason = fields.Text(string='Cancellation Reason')
