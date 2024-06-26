from odoo import models, fields, api, _


class FeesManagement(models.Model):
    _name = 'fees.details'
    _description = 'Maintains student fees Management form'

    room_no = fields.Char(string='Room No', required=True)
    roll_no = fields.Many2one('room.checkin', string='Roll NO', required=True)
    name = fields.Char(string='Name', required=True)
    contact_no = fields.Char(string='Contact NO', required=True)
    department = fields.Char(string='Department NO', required=True)
    fees = fields.Char(string='Fees Amount', required=True)
    mess_charge = fields.Char(string='Mess Charge', required=True)
    miscellaneous = fields.Char(string='Miscellaneous', required=True)
   # penalty = fields.Char(string='Penalty', required=True)
    checkin_Date = fields.Char(string='Checkin Date', required=True)
    payment_status = fields.Char(string='Payment Status', required=True)
    total = fields.Char(string='Total')
    amount_due = fields.Char(string='Due Amount')
    discount_amnt = fields.Char(string='Discount percentage')

    @api.onchange('roll_no')
    def onchange_roll_number(self):
        if self.roll_no:
            partner_record = self.roll_no
            self.name = partner_record.name
            self.contact_no = partner_record.contact_no
            self.department = partner_record.department
            self.fees = partner_record.fees
            self.mess_charge = partner_record.mess_charge
            self.miscellaneous = partner_record.miscellaneous
            self.checkin_Date = partner_record.checkin_Date
            self.payment_status = partner_record.payment_status
            self.room_no = partner_record.room_id.name
            self.total = partner_record.total_charge_with_rupees
            self.amount_due = partner_record.due_amnt  # Make sure due_amnt is a field in room.checkin
            self.discount_amnt = partner_record.discount  # Make sure discount is a field in room.checkin

            # Check if there is a checkout record for the selected roll number
            if partner_record.payment_status == 'yes':
                self.payment_status = 'Paid'
            else:
                self.payment_status = 'Pending'
        else:
            # Clear all other fields if roll_no is False
            self.name = False
            self.contact_no = False
            self.department = False
            self.fees = False
            self.mess_charge = False
            self.miscellaneous = False
            self.checkin_Date = False
            self.payment_status = False
            self.room_no = False
            self.total = False
            self.amount_due = False
            self.discount_amnt = False

    @api.model
    def create(self, vals):
        # Ensure that the penalty field is set to a default value if not provided
        if 'penalty' not in vals:
            vals['penalty'] = '0.00'  # Set a default value here

        # Call the super method to create the record
        return super(FeesManagement, self).create(vals)
