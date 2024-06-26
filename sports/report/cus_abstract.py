from odoo import models, fields, api


class customerReport(models.AbstractModel):
    _name = 'report.sports.report_customer'

    @api.model
    def _get_report_values(self, docids, data):
        start_date = data['s_date']
        end_date = data['e_date']

        records1 = self.env['sports.customer'].browse(data['cus_record_id'])#env[table name]
        return {
            'doc_ids': docids,
            'start_date': start_date,
            'end_date': end_date,
            'records': records1,
        }