from odoo import api, fields, models


class Clct_data_Wizard(models.TransientModel):
    _name = "report.data"

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def wizard_report(self):
        patient_record = self.env['sports.employee'].search(
            [('hire_date', '>=', self.start_date), ('hire_date', '<=', self.end_date)])

        data = {
            's_date': self.start_date,
            'e_date': self.end_date,
            'patient_app_ids': patient_record.ids,
        }
        return self.env.ref('sports.employee_report').report_action(self, data=data)
