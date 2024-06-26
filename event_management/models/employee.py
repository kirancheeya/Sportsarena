from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, date
import random
import string


class Employee(models.Model):
    _name = 'event_management.employee'
    _description = 'Employee Information'

    otp = fields.Char(string='OTP', readonly=True)
    images_1920 = fields.Binary(string='Image', max_width=3500, max_height=2705)
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    country = fields.Many2one('res.country', string='Country')
    country_code = fields.Char(string="country Code")
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    department = fields.Selection(
        [('sales', 'Sales'), ('marketing', 'Marketing'), ('hr', 'Human Resources'), ('it', 'Information Technology')],
        string='Department')
    manager_id = fields.Many2one('event_management.employee', string='Manager')

    # @api.multi
    # def send_email_fun(self):
    #     template = self.env.ref('event_management.event_card_email_template')
    #     for rec in self:
    #         if rec.email:
    #             # Generate OTP
    #             new_otp = self.generate_otp()
    #
    #             # Update OTP field in the record
    #             rec.otp = new_otp
    #
    #             # Send email using the template
    #             template.send_mail(rec.id, force_send=True)

    def send_email_fun(self):
        template = self.env.ref('event_management.event_card_email_template')
        for rec in self:
            if rec.email:
                template.send_mail(rec.id, force_send=True)

    @api.model
    def generate_otp(self, email):
        # Generate a random OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Send OTP via email
        self.send_otp_email(email, otp)

        # Update OTP field in employee record
        employee = self.env['event_management.employee'].search([('email', '=', email)], limit=1)
        employee.write({'otp': otp})

    @api.model
    def send_otp_email(self, email, otp):
        # Send OTP via email
        mail_values = {
            'subject': 'Your OTP for Verification',
            'body_html': f'<p>Your OTP is: <strong>{otp}</strong></p>',
            'email_to': email,
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()

    def validate_otp(self, entered_otp):
        if self.otp != entered_otp:
            raise ValidationError('Invalid OTP. Please enter a valid OTP.')
        # Clear OTP after successful validation
        self.write({'otp': False})

    @api.model
    def create(self, values):
        # Call super to create the record
        new_employee = super(Employee, self).create(values)

        # Send welcome email
        if new_employee.email:
            new_employee.send_welcome_email()

        return new_employee

    def sende_welcome_email(self):
        # Customize the welcome message as per your requirements
        subject = "Welcome to our company!"
        body = f"Dear {self.name},\n\nWelcome to our company! We are excited to have you on board.\n\nBest regards,\nElixer Event Management"

        # Create and send email
        mail_values = {
            'subject': subject,
            'body': body,
            'email_to': self.email,
        }
        self.env['mail.mail'].create(mail_values).send()

    @api.model
    def create(self, vals):
        if self.name:
            vals['name'] = vals.get('name').title()  # upper(), lower()
        return super(Employee, self).create(vals)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Name must be unique!')
    ]

    @api.onchange('country')
    def _onchange_country_id(self):
        if self.country:
            self.country_code = '+' + self.country.code

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                # Check if the entered email is valid
                if not self._is_valid_email(record.email):
                    raise ValidationError('Invalid email format. Please enter a valid email address.')

    def _is_valid_email(self, email):
        # Add your email validation logic here
        # For example, you can use a regular expression to validate the email format
        # Here's a basic example of email validation
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def home(self):
        url_action = self.env['custom.url.action'].create({
            'name': 'Google',
            'url': 'google.com',
            'target': 'new'
        })

    @api.constrains('phone')
    def _check_contact_number_format(self):
        for record in self:
            if record.phone:
                # Define your contact number validation logic here
                # For example, you can use a regular expression to check the format
                import re
                pattern = r'^\+\d{1,2}-\d{3}-\d{3}-\d{4}$'  # Example pattern: +123-456-789-0123
                if not re.match(pattern, record.phone):
                    raise ValidationError('Invalid contact number format. Please enter a valid contact number.')
