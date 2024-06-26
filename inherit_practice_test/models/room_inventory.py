from odoo import models, fields, api


class RoomInventory(models.Model):
    _name = 'room.inventory'
    _description = 'Room Inventory'

    name = fields.Char(string='Item Name', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    room_id = fields.Many2one('room.room', string='Room', required=True)
