from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelRoom(models.Model):
    _name = 'hostel.checkout'
    _description = 'Hostel Room'

    # roll_number = fields.Many2one('student.admission', string='Roll Number', required=True)
    name = fields.Char(string='Name', required=True)
    # department = fields.Char(string='Department', required=True)
    room_no = fields.Char(string='Room No', required=True)
    contact_no = fields.Char(string='Contact')
    remarks = fields.Char(string='Remark')
    penalty = fields.Float(string='Penalty',required=True, default=0.0)
    is_eligible = fields.Boolean(string='Is_eligible', default=True, compute='_compute_is_eligible', store=True)
    check_out_date = fields.Date(string='Check-Out Date')
    due = fields.Char(string='Due Amount', compute='_compute_due', store=True)
    check_in = fields.Many2one('room.checkin', string='checkin',required=True)
    room_details_id = fields.Many2one('hostel.room_details', string='Room Details',required=True)
    check_in_date = fields.Date(sting='check in')

    @api.onchange('check_in')
    def onchange_roll_number(self):
        if self.check_in:
            partner_record = self.check_in
            self.name = partner_record.name
            self.contact_no = partner_record.contact_no
            self.room_no = partner_record.room_id.name
            self.due = partner_record.due_amnt
            self.check_in_date = partner_record.checkin_Date

        else:
            self.name = False
            self.room_no = False
            self.contact_no = False
            self.due = 0.0

    @api.depends('check_in.due_amnt')
    def _compute_due(self):
        for room in self:
            room.due = room.check_in.due_amnt if room.check_in else ''

    @api.depends('due', 'penalty')
    def _compute_is_eligible(self):
        for room in self:
            room.is_eligible = room.due == 0 or room.penalty == 0

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.name:
                existing_checkout = self.search([('name', '=', record.name), ('id', '!=', record.id)])
                if existing_checkout:
                    raise ValidationError(f"A check-out record with the name '{record.name}' already exists.")

    @api.constrains('check_out_date')
    def _check_checkout_date(self):
        for checkout in self:
            if checkout.check_out_date <= checkout.check_in_date:
                raise ValidationError("Check-out date should be after check-in date.")

    def perform_checkout(self):
        for checkout in self:
            if checkout.room_no:
                checkout.room_no.subtract_capacity()
