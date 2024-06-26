from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class CustomerComplaint(models.Model):
    _name = 'customer.complaint'
    _description = 'Customer Complaint'
    _rec_name = 'complain'

    customer_id = fields.Many2one('elixir.customer', string='Customer', required=True)
    complain = fields.Char(string="Complaint Number", readonly=1)
    complaint_date = fields.Datetime(string='Complaint Date', default=fields.Datetime.now, required=True)
    subject = fields.Char(string='Subject', required=True)
    description = fields.Text(string='Description', required=True)
    customer_email = fields.Char(string='Email', required=True)

    @api.constrains('complaint_date')
    def _check_complaint_date(self):
        for complaint in self:
            if complaint.complaint_date.date() != datetime.now().date():
                raise ValidationError("Complaint date must be today.")

    def submit_complaint(self):
        # Perform any additional actions before saving the complaint
        self.create({
            'customer_id': self.customer_id.id,
            'complaint_date': self.complaint_date,
            'subject': self.subject,
            'description': self.description,
        })


    @api.model
    def create(self, vals):
        vals['complain'] = self.env['ir.sequence'].next_by_code('customer.complaint')
        return super(CustomerComplaint, self).create(vals)

    def send_complaint_email(self):
        template = self.env.ref(
            'your_module_name.complaint_email_template')  # Replace 'your_module_name' with your actual module name
        template.send_mail(self.id, force_send=True)


    def send_complaint_email(self):
        template = self.env.ref('elixir_sports_arena.reply_email_template')  # Replace 'your_module_name' with your actual module name
        template.send_mail(self.id, force_send=True)