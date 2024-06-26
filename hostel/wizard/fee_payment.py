from odoo import api, fields, models


class FeesPaymenData(models.TransientModel):
    _name = "report.fees.payment"

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def wizard_fees_report(self):
        cus_record = self.env['hostel_fees_details'].search(
            [('checkin_Date', '>=', self.start_date), ('checkin_Date', '<=', self.end_date)])
#main table for str_date field table name
        data = {
            's_date': self.start_date,
            'e_date': self.end_date,
            'cus_record_id': cus_record.ids,
        }
        return self.env.ref('hostel.billing_invoice_report').report_action(self, data=data)#module name and action id report