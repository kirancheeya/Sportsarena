from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _name = 'event_management.customer'
    _description = 'Customer Information'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    addresses = fields.One2many('event_management.address', 'customer_id', string='Address')
    # city = fields.Char(string='City')
    # country = fields.Char(string='Country')
    dob = fields.Date(string="Date of Birth")
    # age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    str_date = fields.Datetime(string="Current Date")
    orders = fields.One2many('event_management.order', 'customer_id', string='Orders')
    ads = fields.One2many('event_management.address', 'customer_id', string='Address')

    @api.model
    def create(self, vals):
        if self.name:
            vals['name'] = vals.get('name').title()  # upper(), lower()
        return super(Customer, self).create(vals)

    # unique name
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Name must be unique!')
    ]

    # conchange on country code
    @api.onchange('country')
    def _onchange_country_id(self):
        if self.country:
            self.country_code = '+' + self.country.code

    # email validation
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

    # url action
    def home(self):
        url_action = self.env['custom.url.action'].create({
            'name': 'Google',
            'url': 'google.com',
            'target': 'new'
        })

    # contact validation
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


class Address(models.Model):
    _name = 'event_management.address'
    _description = 'Address Information'
    image_1920 = fields.Binary(string='Image', max_width=1000, max_height=705)

    customer_id = fields.Many2one('event_management.customer', string='Customer')
    type = fields.Selection([('billing', 'Billing'), ('shipping', 'Shipping')], string='Type')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    country_id = fields.Many2one('res.country', string='Country')
    zip = fields.Char(string='Zip')
    phone = fields.Char(string='Phone')
    is_default = fields.Boolean(string='Default Address')
