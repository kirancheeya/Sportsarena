from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError
import re


class ElixirEmployee(models.Model):
    _name = 'elixir.employee'
    _description = 'Maintains Employee details'
    _rec_name = 'emp_id'

    emp_id = fields.Char(string="Employee Id", readonly=1)
    name = fields.Char(string='Name', required=True)
    position = fields.Selection(
        [('morning', 'Morning_staff'), ('evening', 'evening Staff'), ('Watchmen', 'Watchmen'), ('Cleaner', 'Cleaner')],
        string='Position', required=True)
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')], string='Gender', required=False)
    dob = fields.Date(string='DOB', required=True)
    age = fields.Integer(string="Age", compute="_get_age", store=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    phone_no = fields.Char(string='Phone No', required=True)
    qualification = fields.Selection([('10th', '10th'), ('12th', '12th'), ('UG', 'UG'), ('PG', 'PG')],
                                     string='Qualification', required=True)
    address_line1 = fields.Char(string='Street1', required=False)
    address_line2 = fields.Char(string='Street2', required=False)
    city = fields.Char(string='City', required=False)
    state = fields.Char(string='State', required=False)
    zip = fields.Char(string='Zip', required=False)
    district = fields.Char(string='District', required=False)
    country = fields.Many2one('res.country', string='Country', required=False)
    email = fields.Char(string='Email', required=True)

    @api.depends('dob')
    def _get_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                self.age = today.year - self.dob.year

    @api.constrains('phone_no')
    def validate_phone(self):
        if self.phone_no:
            phone_len = len(str(self.phone_no))
            if phone_len < 10 or phone_len > 10:
                raise ValidationError("Phone no is incorrect")

    @api.model
    def create(self, vals):
        vals['emp_id'] = self.env['ir.sequence'].next_by_code('elixir.employee')
        return super(ElixirEmployee, self).create(vals)

    def _is_valid_email(self, email):
        return bool(re.match(r'\b[a-z0-9]+@[a-z]+\.[a-z]{2,}\b', email))

    @api.constrains('email')
    def _get_email(self):
        for rec in self:
            if rec.email:
                if not self._is_valid_email(rec.email):
                    raise ValidationError("Invalid email")
