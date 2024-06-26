from odoo import models, fields


class Employee(models.Model):
    _name = 'sports.employee'
    # _inherit = ['hr.employee']
    _description = 'Sports Academy Employee'

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
    job_title = fields.Char('Job Title')
    department = fields.Char('Department')
    salary = fields.Float('Salary')
    hire_date = fields.Date('Hire Date')
    # emp_img = fields.Image('Image', max_width=1000 ,max_height=705)
    image_1920 = fields.Binary(string='Image', max_width=1000, max_height=705)


