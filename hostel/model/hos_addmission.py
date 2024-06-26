from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError
import re


class Hostel(models.Model):
    _name = 'student.admission'
    _description = 'Maintains student admission form'
    _rec_name = 'roll_no'

    roll_no = fields.Char(string="Roll Number", readonly=1)
    first_name = fields.Char(string='First Name', required=True)
    # middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_fullname', store=True)
    dob =\
        fields.Date(string='DOB', required=False)
    admission_date = fields.Date(string='Admission Date', required=False)
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')], string='Gender', required=False)
    status = fields.Selection([
        ('Unapproved', "Unapproved"),
        ('Manager Approved', "Manager Approved"),
        ('Cancelled', "Cancelled"),
    ], string='Status', default='Unapproved')
    age = fields.Integer(string="Age", compute="_get_age", store=True)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    qualification = fields.Selection(
        [('B.A Eng', 'B.A Eng'), ('B.A Tam', 'B.A Tam'), ('B.Sc Mat', 'B.Sc Mat'), ('B.Sc Phy', 'B.Sc Phy'),
         ('B.Sc CS', 'B.Sc CS'), ('B.B.A', 'B.B.A'), ('B.C.A', 'B.C.A')],
        string='Qualification', required=True)
    address_line1 = fields.Char(string='Street1', required=False)
    address_line2 = fields.Char(string='Street2', required=False)
    city = fields.Char(string='City', required=False)
    state = fields.Char(string='State', required=False)
    zip = fields.Char(string='Zip', required=False)
    district = fields.Char(string='District', required=False)
    country = fields.Many2one('res.country', string='Country', required=False)
    blood_group = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], string='Blood Group', required=False)
    languages_known_ids = fields.Many2many('res.lang', string="Language Known", required=True)
    phone_no = fields.Char(string='Phone No', required=False)
    f_name = fields.Char(string='Father Name', required=False)
    proof = fields.Binary(string='Proof', required=False)
    email = fields.Char(string='Email', required=False)
    approved = fields.Boolean(string="Approved", compute="_compute_approval_status", store=True)

    @api.constrains('date_of_birth')
    def _check_age(self):
        for record in self:
            if record.dob:
                min_age_date = datetime.now().date() - timedelta(days=365 * 18)
                if record.dob > min_age_date:
                    raise ValidationError("Applicant must be at least 18 years old.")


    @api.depends('dob')
    def _get_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                dob = fields.Date.from_string(rec.dob)
                rec.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @api.depends('first_name', 'last_name')
    def _compute_fullname(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.full_name = rec.first_name + " " + rec.last_name
            else:
                rec.full_name = False

    @api.constrains('phone_no')
    def validate_phone(self):
        if self.phone_no:
            phone_len = len(str(self.phone_no))
            if phone_len < 10 or phone_len > 10:
                raise ValidationError("Phone no is incorrect")

    def _is_valid_email(self, email):
        return bool(re.match(r'\b[a-z0-9]+@[a-z]+\.[a-z]{2,}\b', email))

    @api.constrains('email')
    def _get_email(self):
        for rec in self:
            if rec.email:
                if not self._is_valid_email(rec.email):
                    raise ValidationError("Invalid email")

    @api.model
    def create(self, vals):
        vals['roll_no'] = self.env['ir.sequence'].next_by_code('hostel.student')
        return super(Hostel, self).create(vals)

    @api.model
    def create(self, vals):
        vals['roll_no'] = self.env['ir.sequence'].next_by_code('hostel.student')
        return super(Hostel, self).create(vals)

    # @api.constrains('admission_date')
    # def _check_admission_date(self):
    #     for record in self:
    #         current_date = datetime.now().date()
    #         if record.admission_date < current_date:
    #             raise ValidationError("Admission date cannot be in the past.")

    @api.depends('status')
    def _compute_approval_status(self):
        for rec in self:
            rec.approved = rec.status == 'Manager Approved'

    def action_approve(self):
        self.status = "Manager Approved"

    def action_cancel(self):
        self.status = "Cancelled"
