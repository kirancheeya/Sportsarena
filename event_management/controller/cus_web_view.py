from odoo import http, _
from odoo.http import request


class Eventcontroller(http.Controller):

    @http.route('/list_employee', type='http', auth='public', website=True)
    def list_employee_data(self):
        emp_ids = request.env['event_management.employee'].search([])
        emp_data = []
        for rec in emp_ids:
            data = {'name': rec.name,
                    'email': rec.email,
                    'phone': rec.phone,
                    'images_1920': rec.images_1920,
                    'address': rec.address,
                    'city': rec.city,
                    'country': rec.country,
                    'country_code': rec.country_code,
                    'gender': rec.gender,
                    'department': rec.department

                    }
            emp_data.append(data)
        return request.render("event_management.emp_list_template", {"emp_data": emp_data})
