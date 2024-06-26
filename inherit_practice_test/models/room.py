from odoo import models, fields, api


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _order = 'sequence'


    SHARING_CONFIGURATIONS = [
        ('single', 'Single Sharing'),
        ('double', 'Double Sharing'),
        ('triple', 'Triple Sharing'),
        ('four', 'Four Sharing')
    ]

    students = fields.One2many('hostel.student', 'room_id', string='Students')
    student = fields.Many2one('hostel.student', string='student')
    name = fields.Char(string='Room ', required=True)
    base_capacity = fields.Integer(string='Base Capacity')
    capacity = fields.Integer(string='Capacity', compute='_compute_capacity', store=True)
    sharing_configuration = fields.Selection(selection=SHARING_CONFIGURATIONS, string='Sharing Configuration')
    base_price = fields.Float(string='Base Price')
    price = fields.Float(string='Price', compute='_compute_price', store=True)
    availability = fields.Boolean(string='Availability', default=True)
   # sequence = fields.Char(string='Room Number', copy=False, readonly=True,
                           #default=lambda self: self.env['ir.sequence'].next_by_code('hostel.room.sequence'))

    # Add this field


    @api.depends('sharing_configuration', 'students')
    def _compute_capacity(self):
        for room in self:
            if room.sharing_configuration == 'single':
                room.capacity = 1
            elif room.sharing_configuration == 'double':
                room.capacity = 2
            elif room.sharing_configuration == 'triple':
                room.capacity = 3
            elif room.sharing_configuration == 'four':
                room.capacity = 4
            else:
                room.capacity = room.base_capacity

    @api.onchange('sharing_configuration')
    def _onchange_sharing_configuration(self):
        # When the sharing configuration changes, reset the students assigned to the room
        self.students = False

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
