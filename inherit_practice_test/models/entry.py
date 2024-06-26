from odoo import models, fields, api


class Entry(models.Model):
    _name = 'entry.entry'
    _description = 'Entry'

    name = fields.Char(string='Entry Name', required=True)
    entry_time = fields.Datetime(string='Entry Time', required=True)
    noc_status = fields.Many2one('', string='NOC', required=True)
    #student_id = fields.Many2one('res.partner', string='Person', required=True)(student_id)
    #adminision_id = fields.Many2one('', string='Admission number', required=True)(adminision_id)
    #department_id = fields.Many2one('', string='Department', required=True)(adminision_id)
    proof = fields.Binary(string="Proof")


