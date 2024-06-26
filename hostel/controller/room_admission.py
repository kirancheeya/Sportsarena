from odoo import http, _
from odoo.http import request


class HostelController(http.Controller):

    @http.route('/list_st_admission', type='http', auth='user', website=True)
    def list_admission_details(self):
        students_admm_ids = request.env['student.admission'].search([])
        student_data = []
        for rec in students_admm_ids:
            data = {
                'full_name': rec.first_name,
                'gender': rec.gender,
                'dob': rec.dob,
                'admission_date': rec.admission_date,
                'qualification': rec.qualification,
                'blood_group': rec.blood_group,
                'phone_no': rec.phone_no,
                'email': rec.email
            }
            student_data.append(data)
        return request.render("hostel.student_adm_list_template", {"student_data": student_data})

    @http.route('/student_adm_registration', auth='public', type='http', website=True)
    def admission_form(self):
        return request.render("hostel.student_adm_registration_template")

    @http.route('/ad_student', auth='public', type='http', website=True)
    def add_admission(self, **k):
        print('k', k)
        name = k['first_name']
        name1 = k['last_name']
        gender = k['gender']
        dob = k['dob']
        admission = k['admission_date']
        qualification = k['qualification']
        blood = k['blood_group']
        phone = k['phone_no']
        email = k['email']

        request.env['student.admission'].create({
            'first_name': name, 'last_name': name1, 'qualification': qualification, 'gender': gender, 'dob': dob,
            'admission_date': admission,
            'blood_group': blood, 'phone_no': phone, 'email': email}),
        return request.render("hostel.admission_success", {})
