from odoo import models, fields, api


class HostelStudent(models.Model):
    _name = 'hostel.st'
    _description = 'Hostel Student'
    _rec_name = 'roll_number'

    name = fields.Char(string='Name', required=True)
    roll_number = fields.Char(string='Roll Number', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    checkin_id = fields.Many2one('hostel.checkin', string='Room')

    @api.model
    def create(self, vals):
        student = super(HostelStudent, self).create(vals)
        if student.checkin_id:
            student.checkin_id.update_current_capacity()
        return student


