from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelRoom(models.Model):
    _name = 'hostel.room_details'
    _description = 'Hostel Room'

    name = fields.Char(string='Room No', required=True)
    base_capacity = fields.Integer(string='Base Capacity', default=2)
    current_capacity = fields.Integer(string='Current Capacity', compute='_compute_capacity', store=True)
    availability = fields.Boolean(string='Availability', compute='_compute_capacity', store=True)
    checkin_ids = fields.One2many('room.checkin', 'room_id', string='Check-ins')
    check_out_ids = fields.One2many('hostel.checkout', 'room_details_id', string='Check Outs')

    # @api.depends('checkin_ids')
    # def _compute_current_capacity(self):
    #     for room in self:
    #         room.current_capacity = len(room.checkin_ids)
    # less

    # Compute method to calculate current capacity and availability of the room
    @api.depends('checkin_ids')
    def _compute_capacity(self):
        for room in self:
            room.current_capacity = len(room.checkin_ids)
            if room.current_capacity < room.base_capacity:
                room.availability = True
            elif room.current_capacity == room.base_capacity:
                room.availability = False
            else:
                room.availability = False
            print("Room", room.name, "Current Capacity:", room.current_capacity, "Availability:", room.availability)

    def subtract_capacity(self):
        if self.current_capacity > 0:
            self.current_capacity -= 1

    @api.depends('base_capacity', 'current_capacity')
    def _compute_availability(self):
        for room in self:
            room.availability = room.current_capacity < room.base_capacity

    def update_current_capacity(self):
        self._compute_capacity()
        self._compute_availability()

    @api.constrains('current_capacity', 'base_capacity')
    def _check_room_capacity(self):
        for room in self:
            if room.current_capacity > room.base_capacity:
                available_rooms = self.env['hostel.room_details'].search([('availability', '=', True)])
                if available_rooms:
                    available_room_names = ', '.join(room.name for room in available_rooms)
                    raise ValidationError(
                        "Room capacity exceeded. Please choose another room. Available rooms: %s" % available_room_names)
                else:
                    raise ValidationError("Room capacity exceeded. There are no available rooms.")

    # Compute method to calculate current capacity and availability of the room

    def subtract_capacity(self):
        if self.current_capacity > 0:
            self.current_capacity -= 1
