from odoo import api, fields, models, _
from datetime import datetime, date


class Payment(models.Model):
    _name = 'payment.details'
    _description = 'maintaining the payment details'
    _rec_name = 'guest_name'

    guest_name = fields.Char(string='Guest name', required=True)
    check_in = fields.Date(string='Check In', required=True)
    check_out = fields.Date(string='Check Out', required=True)
    days_of_stay = fields.Integer(string='Days Of Stay', compute='compute_duration_date', store=True)
    room_type_id = fields.Many2one('room.category', string='Room Type', required=True)
    day_price = fields.Float(string='Per Day Charge', required=True)
    amount = fields.Float(string='Total Staying Charge', compute='compute_total_amount', store=True)
    event_name_ids = fields.Many2many('service.details', string='Available Events ')
    events_price = fields.Float(string='Events Cost', compute='_compute_event_amount', store=True)
    damage_name_ids = fields.Many2many('damage.details', string='Damages')
    damage_price = fields.Float(string='Damages Price', compute='compute_damage_price')
    discount_id = fields.Many2one('discount.details', string='Discount')
    discount_amount = fields.Float(string='Discount Amount', compute='discount_id_onchange')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    payment = fields.Selection(
        [('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer'),
         ('Online Payment', 'Online Payment')], string='Payment_mode', required=True)

    @api.onchange('room_type_id')
    def room_type_id_onchange(self):
        if self.room_type_id:
            self.day_price = self.room_type_id.price

    @api.onchange('discount_id')
    def discount_id_onchange(self):
        if self.discount_id:
            self.discount_amount = self.discount_id.deduction

    @api.depends('check_in', 'check_out')
    def compute_duration_date(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                day = rec.check_out - rec.check_in
                rec.days_of_stay = day.days

    @api.depends('days_of_stay', 'day_price')
    def compute_total_amount(self):
        for rec in self:
            rec.amount = rec.days_of_stay * rec.day_price

    @api.depends('event_name_ids')
    def _compute_event_amount(self):
        for rec in self:
            rec.events_price = sum(rec.event_name_ids.mapped('amount'))

    @api.depends('amount', 'events_price', 'discount_amount', 'damage_price')
    def _compute_total_amount(self):
        for payment in self:
            payment.total_amount = (payment.amount + payment.events_price + payment.damage_price - payment.
                                    discount_amount)

