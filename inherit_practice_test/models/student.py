from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HostelStudent(models.Model):
    _name = 'hostel.student'
    _description = 'Hostel Student'

    name = fields.Char(string='Name', required=True)
    roll_number = fields.Char(string='Roll Number', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    room_id = fields.Many2one('hostel.room', string='Room')

    @api.constrains('room_id')
    def _check_room_capacity(self):
        for student in self:
            if student.room_id and len(student.room_id.students) > student.room_id.capacity:
                raise ValidationError("Room capacity exceeded. Please choose another room.")
