from odoo import models, fields, api


class Management(models.Model):
    _name = 'management.info'

    name = fields.Char('Name', required=True)
    user_id = fields.Many2one('res.users', string='Responsible', required=True)
