from odoo import models, fields, api


class Expense(models.Model):
    _name = 'event_management.expense'
    _description = 'Expense Information'

    name = fields.Char(string='Expense Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    employee_id = fields.Many2one('event_management.employee', string='Employee')
    category = fields.Selection(
        [('travel', 'Travel'), ('entertainment', 'Entertainment'), ('office_supplies', 'Office Supplies'),
         ('miscellaneous', 'Miscellaneous')], string='Category')
    status = fields.Selection(
        [('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        string='Status')
