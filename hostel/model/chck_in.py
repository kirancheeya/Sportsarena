from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelRoom(models.Model):
    _name = 'hostel.checkin'
    _description = 'Hostel Room'

    SHARING_CONFIGURATIONS = [
        ('single', 'Single Sharing'),
        ('double', 'Double Sharing'),
        ('triple', 'Triple Sharing'),
        ('four', 'Four Sharing')
    ]

    student_ids = fields.One2many('hostel.st', 'checkin_id', string='student')
    name = fields.Char(string='Room No', required=True)
    sharing_configuration = fields.Selection(selection=SHARING_CONFIGURATIONS, string='Sharing Configuration')
    base_capacity = fields.Integer(string='Base Capacity', compute='_compute_base_capacity', store=True)
    capacity = fields.Integer(string='Current Capacity', compute='_compute_current_capacity', store=True)
    base_price = fields.Float(string='Base Price')
    price = fields.Float(string='Price', compute='_compute_price', store=True)
    availability = fields.Boolean(string='Availability', compute='_compute_availability', store=True)


    # mother_lang = fields.Many2one('res.lang', string="mother language")
    # ml = fields.Many2many('res.lang', string='l')

    @api.depends('sharing_configuration')
    def _compute_base_capacity(self):
        for room in self:
            if room.sharing_configuration == 'single':
                room.base_capacity = 1
            elif room.sharing_configuration == 'double':
                room.base_capacity = 2
            elif room.sharing_configuration == 'triple':
                room.base_capacity = 3
            elif room.sharing_configuration == 'four':
                room.base_capacity = 4
            else:
                room.base_capacity = 0

    @api.depends('student_ids')
    def _compute_current_capacity(self):
        for room in self:
            room.capacity = len(room.student_ids)

    @api.depends('base_capacity', 'capacity')
    def _compute_availability(self):
        for room in self:
            room.availability = room.capacity <= room.base_capacity

    def update_current_capacity(self):

        self._compute_current_capacity()
        self._compute_availability()

    @api.constrains('capacity', 'base_capacity')
    def _check_room_capacity(self):
        for room in self:
            if room.capacity > room.base_capacity:
                available_rooms = self.env['hostel.checkin'].search([('availability', '=', True)])
                available_room_names = ', '.join(room.name for room in available_rooms)
                raise ValidationError(
                    "Room capacity exceeded. Please choose another room. Available rooms: %s" % available_room_names)

    @api.depends('base_price', 'sharing_configuration')
    def _compute_price(self):
        for room in self:
            if room.sharing_configuration == 'single':
                room.price = room.base_price * 1.2
            elif room.sharing_configuration == 'double':
                room.price = room.base_price
            elif room.sharing_configuration == 'triple':
                room.price = room.base_price * 0.8
            elif room.sharing_configuration == 'four':
                room.price = room.base_price * 0.6  # Adjusting price for four sharing
            else:
                room.price = room.base_price
