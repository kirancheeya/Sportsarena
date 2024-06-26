from odoo import models, fields, api, exceptions
from datetime import timedelta
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz


class Booking(models.Model):
    _name = 'elixir.booking'
    _description = 'Booking for Badminton Court'

    PREDEFINED_TIMES = [
        ('06:00', '6:00 AM - 7:00 AM'),
        ('07:00', '7:00 AM - 8:00 AM'),
        ('08:00', '8:00 AM - 9:00 AM'),
        ('09:00', '9:00 AM - 10:00 AM'),
        ('10:00', '10:00 AM - 11:00 AM'),
        ('11:00', '11:00 AM - 12:00 PM'),
        ('12:00', '12:00 PM - 1:00 PM'),
        ('13:00', '1:00 PM - 2:00 PM'),
        ('14:00', '2:00 PM - 3:00 PM'),
        ('15:00', '3:00 PM - 4:00 PM'),
        ('16:00', '4:00 PM - 5:00 PM'),
        ('17:00', '5:00 PM - 6:00 PM'),
        ('18:00', '6:00 PM - 7:00 PM'),
        ('19:00', '7:00 PM - 8:00 PM'),
        ('20:00', '8:00 PM - 9:00 PM'),
        ('21:00', '9:00 PM - 10:00 PM'),
        ('22:00', '10:00 PM - 11:00 PM'),
        ('23:00', '11:00 PM - 12:00 AM'),
    ]
    booking_no = fields.Char(string='Booking No', readonly=1)
    customer_id = fields.Many2one('elixir.customer', string='Customer', required=True)
    customer_name = fields.Char(string='Contact Name')
    cus_contact = fields.Char('Contact Contact')
    cus_email = fields.Char('Customer Email')
    employee_id = fields.Many2one('elixir.employee', string='Employee', required=True)
    emp_name = fields.Char(string='Employee Name', required=True)
    court_id = fields.Many2one('elixir.badminton_court', string='Badminton Court')

    is_paid = fields.Boolean('Is Paid', default=False)
    sports = fields.Selection([('badminton', 'Badminton'),
                               ('swimming', 'Swimming'),
                               ('tt', 'TT')])
    price = fields.Char(string='Court Price')
    start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
    end_time = fields.Datetime(string='End Time', default=lambda self: fields.Datetime.now() + timedelta(hours=1))
    court_type = fields.Char(string='Court Type')

    stopwatch_running = fields.Boolean('Stopwatch Running', default=False)
    stopwatch_start_time = fields.Datetime('Stopwatch Start Time')
    stopwatch_elapsed_time = fields.Float('Elapsed Time (seconds)', compute='_compute_remaining_time',
                                          store=True)
    remaining_time = fields.Char('Remaining Time', compute='_compute_remaining_time', store=True)
    predefined_time = fields.Selection(PREDEFINED_TIMES, string='Predefined Time')
    tt_court_id = fields.Many2one('elixir.tt_court', String='Table Tennis Court ')
    tt_court_type = fields.Char(string='CourtS type')
    swimming_id = fields.Many2one('elixir.swimming_pool_court', String='Swimming')
    swimming_type = fields.Char(string='CourtS type')
    racket_bookings = fields.Many2many('sports.inventory', string='Racket Bookings')
    rent_price = fields.Char(string='Rent Price', compute='_compute_rent_price', store=True)
    quantity = fields.Integer(string='Quantity')
    total = fields.Char(string='Total', compute='_compute_total_price', store=True)
    status = fields.Selection([('draft', 'Draft'),
                               ('approved', 'Approved'),
                               ('cancellation', 'Canceled')], default='draft')

    total_amt = fields.Char(string='Total Amount')
    discount = fields.Float(string='Discount (%)', default=0.0)
    # Your existing fields and methods...



    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)
        booking._check_court_availability()
        return booking

    def write(self, vals):
        res = super(Booking, self).write(vals)
        for booking in self:
            booking._check_court_availability()
        return res

    # def _check_court_availability(self):
    #     for booking in self:
    #         court = booking.court_id
    #         if court:
    #             booked_time_slots = self.env['elixir.booking'].search([
    #                 ('court_id', '=', court.id),
    #                 ('predefined_time', '!=', False),
    #                 ('id', '!=', booking.id),  # Exclude the current booking
    #             ]).mapped('predefined_time')
    #
    #             if booking.predefined_time in booked_time_slots:
    #                 available_slots = [slot[0] for slot in booking.PREDEFINED_TIMES if slot[0] not in booked_time_slots]
    #                 if not available_slots:
    #                     raise exceptions.ValidationError(
    #                         f'Court is not available for the selected time slot ({booking.predefined_time}). '
    #                         f'There are no available time slots for this court. Please choose another court or time.'
    #                     )
    #
    #                 available_slots_str = ', '.join(available_slots)
    #                 raise exceptions.ValidationError(
    #                     f'Court is not available for the selected time slot ({booking.predefined_time}). '
    #                     f'Available time slots: {available_slots_str}. Please choose another time.'
    #                 )

    @api.onchange('court_id', )
    def onCustomerChange_price(self):
        if self.court_id:
            self.price = self.court_id.price_per_hour
            self.court_type = self.court_id.court_type

    @api.onchange('tt_court_id', )
    def onCustomerChange_TT(self):
        if self.tt_court_id:
            self.price = self.tt_court_id.indoor_price_per_hour
            self.tt_court_type = self.tt_court_id.court_type

    @api.onchange('swimming_id', )
    def onCustomerChange_swimming(self):
        if self.swimming_id:
            self.price = self.swimming_id.indoor_price_per_hour
            self.swimming_type = self.swimming_id.pool_type

    def _check_court_availability(self):
        for booking in self:
            court = False
            if booking.court_id:
                court = booking.court_id
            elif booking.tt_court_id:
                court = booking.tt_court_id

            if court:
                booked_time_slots = self.env['elixir.booking'].search([
                    '|',
                    ('court_id', '=', court.id),
                    ('tt_court_id', '=', court.id),
                    ('predefined_time', '!=', False),
                    ('id', '!=', booking.id),  # Exclude the current booking
                ]).mapped('predefined_time')

                if booking.predefined_time in booked_time_slots:
                    available_slots = [slot[0] for slot in self.PREDEFINED_TIMES if slot[0] not in booked_time_slots]
                    if not available_slots:
                        raise exceptions.ValidationError(
                            f'Court is not available for the selected time slot ({booking.predefined_time}). '
                            f'There are no available time slots for this court. Please choose another court or time.'
                        )

                    available_slots_str = ', '.join(available_slots)
                    raise exceptions.ValidationError(
                        f'Court is not available for the selected time slot ({booking.predefined_time}). '
                        f'Available time slots: {available_slots_str}. Please choose another time.'
                    )

    # @api.depends('racket_bookings.quantity', 'racket_bookings.rental_price')
    # def _compute_rent_price(self):
    #     for booking in self:
    #         total_rent_price = sum(racket.quantity * racket.rental_price for racket in booking.racket_bookings)
    #         booking.rent_price = total_rent_price

    @api.depends('quantity', 'racket_bookings.rental_price')
    def _compute_rent_price(self):
        for booking in self:
            total_rent_price = sum(self.quantity * racket.rental_price for racket in booking.racket_bookings)
            booking.rent_price = total_rent_price

    @api.depends('rent_price', 'price')
    def _compute_total_price(self):
        for booking in self:
            total_price = (self._convert_to_numeric(booking.rent_price) or 0) + self._convert_to_numeric(booking.price)
            booking.total = total_price

    def _convert_to_numeric(self, value):
        try:
            return float(value) if value else 0
        except ValueError:
            return 0

    @api.onchange('is_paid')
    def _onchange_is_paid(self):
        if self.is_paid:
            if self.status == 'draft':
                self.status = 'approved'

    def action_cancel(self):
        for booking in self:
            if booking.status == 'approved':
                booking.status = 'cancellation'
            elif booking.status == 'draft':
                booking.status = 'cancellation'

                self.env['elixir.cancellation.details'].create({
                    'booking_no': booking.booking_no,
                    'customer_id': booking.customer_id.id,
                    'employee_id': booking.employee_id.id,
                    'reason': booking.reason
                })

    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)
        if booking.is_paid:
            booking.status = 'approved'
        return booking

    def write(self, vals):
        res = super(Booking, self).write(vals)
        if 'is_paid' in vals:
            for booking in self:
                if booking.is_paid and booking.status == 'draft':
                    booking.status = 'approved'
        return res

    @api.depends('quantity', 'racket_bookings.rental_price', 'price', 'discount')
    def _compute_total_price(self):
        for booking in self:
            total_rent_price = sum(booking.quantity * racket.rental_price for racket in booking.racket_bookings)
            total_court_price = self._convert_to_numeric(booking.price)
            subtotal = total_rent_price + total_court_price
            discount_amount = (subtotal * booking.discount) / 100.0
            total_with_discount = subtotal - discount_amount
            booking.total = total_with_discount

    @api.onchange('employee_id', )
    def onCustomerChadnge(self):
        if self.employee_id:
            self.emp_name = self.employee_id.name

    @api.onchange('customer_id', )
    def onCustomerChange(self):
        if self.customer_id:
            self.customer_name = self.customer_id.full_name
            self.cus_contact = self.customer_id.phone_no
            self.cus_email = self.customer_id.email

    @api.model
    def create(self, vals):
        vals['booking_no'] = self.env['ir.sequence'].next_by_code('elixir.booking')
        return super(Booking, self).create(vals)

