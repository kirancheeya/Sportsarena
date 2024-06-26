from odoo import models, fields, api
from odoo.exceptions import ValidationError
import smtplib

class Booking(models.Model):
    _name = 'sports.booking'
    _description = 'Booking for Badminton Court'

    customer_id = fields.Many2one('sports.customer', string='Customer', required=True)
    # customer_contact_id = fields.Many2one('sports.customer', string='Contact Person')
    cus_contact = fields.Char('Contact Person')
    employee_id = fields.Many2one('sports.employee', string='Employee', required=True)
    court_id = fields.Many2one('sports.badminton_court', string='Court', required=True)
    start_time = fields.Datetime('Start Time', required=True)
    end_time = fields.Datetime('End Time', required=True)
    is_paid = fields.Boolean('Is Paid', default=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')],default='draft')

    @api.onchange('customer_id')
    def onCustomerChange(self):
        if self.customer_id:
            self.cus_contact = self.customer_id.phone

    @api.constrains('start_time', 'end_time')
    def _check_start_end_time(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("Start time must be before end time!")

    def move_approved(self):
        self.state = 'approved'

        x = smtplib.SMTP('smtp.gmail.com', 587)
        print(x)
        x.starttls()
        x.login("kiranraj.ds00661@gmail.com", "antu zepg kqtb uxru")
        message = "thanks for coming to yelagiri hills"
        x.sendmail("kiranraj.ds00661@gmail.com", ["rubandoss.ruban"], message)
        x.quit()