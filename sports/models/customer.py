from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests


class Customer(models.Model):
    _name = 'sports.customer'
    _description = 'Sports Academy Customer'

    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    address = fields.Text('Address')
    date_of_birth = fields.Date('Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    str_date = fields.Date('Members of GSA')
    emergency_contact_name = fields.Char('Emergency Contact Name')
    emergency_contact_phone = fields.Char('Emergency Contact Phone')
    medical_conditions = fields.Text('Medical Conditions')
    message = fields.Text(string='Message')

    def send_whatsapp_message(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://web.whatsapp.com/',
            'target': 'new'
        }

    # email validation

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Invalid email address.")

    @api.model
    def create(self, vals):
        if self.name:
            vals['name'] = vals.get('name').title()  # upper(), lower()
        return super(Customer, self).create(vals)
