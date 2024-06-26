from odoo import api, fields,models,_
#info details

class Employee_filter(models.TransientModel):
    _name = "employee.filter"
    _description = "Employee filter wizard"
    #
    # start_time = fields.Datetime("Start Time", required=True)
    # end_time = fields.Datetime("End Time", required=True)
    # court_num = fields.Many2one('sports.badminton_court', 'Court no', required=True)
    # emp_name = fields.Many2one('Sports Academy Employee', 'Employee Name', required=True)
    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Phone')
    address = fields.Text('Address')

    def create_employee_action(self):
        print("button is clicked")
        # vals = {
        #     'date_appointment': self.date_appointment,
        #     'patient_id': self.patient_id.id,
        #     'doctor_id': self.doctor_id.id,
        # }
        employee_rec = self.env['sports.employee'].create(
            {'name': self.name,
             'email': self.email,
             'phone': self.phone,
             'address': self.address})

        return {
            'name': _('Employee filter'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sports.employee',
            'res_id': employee_rec.id,
        }