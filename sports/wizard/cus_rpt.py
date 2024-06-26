from odoo import api, fields, models


class Clct_cus_data(models.TransientModel):
    _name = "report.cus.data"

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def wizard_cus_report(self):
        cus_record = self.env['sports.customer'].search(
            [('str_date', '>=', self.start_date), ('str_date', '<=', self.end_date)])
#main table for str_date field table name
        data = {
            's_date': self.start_date,
            'e_date': self.end_date,
            'cus_record_id': cus_record.ids,
        }
        return self.env.ref('sports.customer_report').report_action(self, data=data)#module name and action id report