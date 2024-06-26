from odoo import models, fields, api


class Event(models.Model):
    _name = 'event_management.event'
    _description = 'Event Information'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    location = fields.Char(string='Location')
    attendees = fields.Many2many('event_management.customer', string='Attendees')
