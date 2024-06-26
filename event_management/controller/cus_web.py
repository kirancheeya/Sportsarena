from odoo import http, _
from odoo.http import request


class EventcontrollerCus(http.Controller):

    @http.route('/customer_registration', auth='user', type='http', website=True)
    def registration_form(self):
        cus_ids = request.env['event_management.customer'].search([])
        print('cus_ids', cus_ids)
        return request.render("event_management.customer_registration_template", {"cus_ids": cus_ids})

    @http.route('/add_customer', auth='user', type='http', website=True)

    def add_admission(self, **k):
        print('k', k)
        name = k['name']
        cus_id = k['cus_id']

        request.env['student.profile'].create({
            'name': name, 'department_id': cus_id
        })
        return request.render("event_management.admission_success", {})
