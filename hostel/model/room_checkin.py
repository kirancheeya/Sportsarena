
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelRoom(models.Model):
    _name = 'room.checkin'
    _description = 'Hostel Room'
    _rec_name = 'ad_id'

    ad_id = fields.Many2one('student.admission', string='Roll No', required=True)
    name = fields.Char(string='Name', required=True)
    contact_no = fields.Char(string='Contact', required=True, invisible=True)
    department = fields.Char(string='Department', required=True)

    fees = fields.Float(string='Room Fees', required=True, default=3500)
    mess_charge = fields.Float(string='Mess Charge', required=True, default=2000)
    miscellaneous = fields.Float(string='Miscellaneous Charge', required=True, default=200)
    checkin_Date = fields.Datetime(string='Check In Date')
    payment_status = fields.Selection([('yes', 'Paid'), ('no', 'Pending')], compute='_compute_payment_status', store=True)
    total = fields.Float(string='Total charge', compute='_compute_total_charge', store=True)
    total_charge_with_rupees = fields.Char(string='Total Charge with Rupees', compute='_compute_total_charge_with_rupees', store=True)
    room_id = fields.Many2one('hostel.room_details', string='Room')
    amt_paid = fields.Float(string='Amount Paid')
    due_amnt = fields.Float(string='Due Amount', compute='compute_due', store=True)
    discount = fields.Float(string='Discount (%)', default=0.0)
    check_out_id = fields.Many2one('hostel.checkout', string='Checkout_details')

    @api.model
    def create(self, vals):
        student = super(HostelRoom, self).create(vals)
        if student.room_id:
            student.room_id.update_current_capacity()
        return student

    @api.depends('total')
    def _compute_total_charge_with_rupees(self):
        for rec in self:
            rec.total_charge_with_rupees = '₹ {:.2f}'.format(rec.total)

    @api.depends('total', 'amt_paid')
    def compute_due(self):
        for rec in self:
            if rec.total and rec.amt_paid:
                due = rec.total - rec.amt_paid
                rec.due_amnt = due

    @api.onchange('ad_id')
    def onchange_roll_number(self):
        if self.ad_id:
            partner_record = self.ad_id
            self.name = partner_record.full_name
            self.contact_no = partner_record.phone_no
            self.department = partner_record.qualification
        else:
            self.name = False
            self.contact_no = False

    @api.depends('mess_charge', 'fees', 'miscellaneous', 'discount')
    def _compute_total_charge(self):
        for room in self:
            total_charge = room.fees + room.mess_charge + room.miscellaneous
            discount_amount = (total_charge * room.discount) / 100.0
            room.total = total_charge - discount_amount

    @api.depends('total', 'amt_paid')
    def _compute_payment_status(self):
        for record in self:
            if record.total and record.amt_paid:
                if record.total == record.amt_paid:
                    record.payment_status = 'yes'
                else:
                    record.payment_status = 'no'
            else:
                record.payment_status = 'no'
