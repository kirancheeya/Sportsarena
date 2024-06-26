from odoo import models, fields, api


class Task(models.Model):
    _name = 'event_management.task'
    _description = 'Task Information'

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    employee_id = fields.Many2one('event_management.employee', string='Assigned Employee')
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Priority')
    status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
                              string='Status')
