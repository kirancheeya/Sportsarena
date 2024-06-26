from odoo import models, fields, api, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class HostelManager(models.Model):
    _name = 'manager.details'
    _description = 'Maintains hostel room details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    shift = fields.Selection([('Morning shift', 'Morning shift'), ('Night shift', 'Night shift')], string='Shift', required=True )
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')], string='Gender', required=False)
    dob = fields.Date(string='DOB', required=True)
    age = fields.Integer(string="Age", compute="_get_age", store=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    phone_no = fields.Char(string='Phone No', required=True)
    qualification = fields.Selection([('10th', '10th'), ('12th', '12th'), ('UG', 'UG'), ('PG', 'PG')], string='Qualification', required=True)
    address_line1 = fields.Char(string='Street1', required=False)
    address_line2 = fields.Char(string='Street2', required=False)
    city = fields.Char(string='City', required=False)
    state = fields.Char(string='State', required=False)
    zip = fields.Char(string='Zip', required=False)
    district = fields.Char(string='District', required=False)
    country = fields.Many2one('res.country', string='Country', required=False)
    experience = fields.Char(string='Experience', required=True)

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


