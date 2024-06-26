from odoo import models, fields, api


class EmloyeeReport(models.AbstractModel):
    _name = 'report.sports.report_employee'

    @api.model
    def _get_report_values(self, docids, data):
        start_date = data['s_date']
        end_date = data['e_date']

        records = self.env['sports.employee'].browse(data['patient_app_ids'])
        return {
            'doc_ids': docids,
            'start_date': start_date,
            'end_date': end_date,
            'records': records,
        }
