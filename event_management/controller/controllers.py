from odoo import http, _
from odoo.http import request


class SchoolController(http.Controller):
    @http.route('/employee_registration', auth='user', type='http', website=True)
    def employee_form(self):
        country_id = request.env['res.country'].search([])
        print('country_id', country_id)
        return request.render("event_management.employe_registration_template", {"country_id": country_id})

    @http.route('/add_employee', auth='user', type='http', website=True)
    def add_employee(self, **k):
        print('k', k)
        country = k['country']
        name = k['name']
        email = k['email']
        phone_no = k['phone']
        city = k['city']

        request.env['event_management.employee'].create({
            'country': country, 'name': name, 'email': email, 'phone': phone_no, 'city': city
        })
        return request.render("event_management.admission_success", {})

    @http.route('/add_customer', auth='user', type='http', website=True)
    def add_employee(self, **k):
        print('k', k)
        name = k['name']
        email = k['email']
        phone = k['phone']
        dob = k['dob']
        gender = k['gender']
        str_date = k['str_date']
        city = k['city']

        request.env['event_management.customer'].create({
            'name': name, 'email': email, 'phone': phone, 'dob': dob, 'gender': gender, 'str_date': str_date,
            'city': city
        })
        return request.render("event_management.admission_success", {})
