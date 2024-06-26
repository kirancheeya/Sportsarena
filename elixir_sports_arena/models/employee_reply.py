from odoo import models, fields, api
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError


class EmployeeReply(models.Model):
    _name = 'employee.reply'
    _description = 'employee Reply'

    feedback_id = fields.Many2one('customer.complaint', string='Feedback', required=True)
    employee_id = fields.Many2one('elixir.employee', string='Employee', required=True)
    reply_text = fields.Text(string="Reply", required=True)
    date_sent = fields.Datetime(string="Date Sent", default=fields.Datetime.now, readonly=True)
    emp_email = fields.Char(srting="Email", required=True)
    emp_Cus = fields.Char(srting="Customer Email", required=True)
    subject = fields.Char(string="Subject", required=True)
    description = fields.Text(string="Description", required=True)
    position = fields.Char(string="Position", required=True)
    name = fields.Char(string="Name", require=True)
    feedback = fields.Many2one('customer.complaint',string="Complaint Number", require=True)

    @api.onchange('employee_id')
    def onchange_emloyee_id(self):
        if self.employee_id:
            partner_record = self.employee_id
            self.name = partner_record.name
            self.position = partner_record.position
            self.emp_email = partner_record.email

    @api.onchange('feedback_id')
    def onchange_feedback_id(self):
        if self.feedback_id:
            partner_record = self.feedback_id
            self.emp_Cus = partner_record.customer_email

    def send_reply_email(self):
        if not (self.employee_id and self.feedback_id):
            raise ValidationError("Employee and Feedback must be set before sending the email.")
        template = self.env.ref('elixir_sports_arena.reply_email_template')
        template.send_mail(self.id, force_send=True)
