from odoo import models, fields, api


class InvoiceBooking(models.AbstractModel):
    _name = 'report.elixir_sports_arena.invoice_booking_customer'

    @api.model
    def _get_report_values(self, docids, data):
        start_date = data['s_date']
        end_date = data['e_date']

        records = self.env['elixir.booking'].browse(data['patient_app_ids'])
        return {
            'doc_ids': docids,
            'start_date': start_date,
            'end_date': end_date,
            'records': records,
        }