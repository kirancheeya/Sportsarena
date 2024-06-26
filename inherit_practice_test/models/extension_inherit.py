from odoo import models, fields, api


class InheritUsers(models.Model):
    _inherit = 'sports.customer'

    test_inherit = fields.Char(string="Test")
