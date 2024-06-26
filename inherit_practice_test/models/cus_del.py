from odoo import models, fields, api


class DelBook(models.Model):
    _name = 'del.booking.info'
    _description = 'booking details'
    _inherits = {'sports.employee': 'emp_id'}

    name = fields.Char(string='Employeee Name')
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')], string='Gender')
    emp_id = fields.Many2one(comodel_name='sports.employee', string='Employee', required=False,ondelete='cascade')