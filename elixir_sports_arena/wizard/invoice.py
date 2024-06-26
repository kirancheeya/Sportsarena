from odoo import api, fields, models


class InvoiceBookingCus(models.TransientModel):
    _name = "report.invoice"

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def wizard_report(self):
        patient_record = self.env['elixir.booking'].search(
            [('start_time', '>=', self.start_date), ('start_time', '<=', self.end_date)])

        data = {
            's_date': self.start_date,
            'e_date': self.end_date,
            'patient_app_ids': patient_record.ids,
        }
        return self.env.ref('elixir_sports_arena.invoice_booking').report_action(self, data=data)
