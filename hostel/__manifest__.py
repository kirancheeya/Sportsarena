{
    'name': "BOSCO HOSTEL",
    'Sequence': 1,
    'version': '1.0',
    'category': 'HOSTEL',
    'website': 'www.hostel.com',
    'summary': "Sports Arena",
    'data': [
        'report\hostel_admission_collection.xml',
        'data\hostel_admission.xml',
        'data\hroom_avalable_template.xml',
        'data\ir_sequence.xml',
        # 'data\h_report_action.xml',
        'security\ir.model.access.csv',
        'views\check_out.xml',
        'views\hos_admission.xml',
        'views\hostel_room_checkin.xml',
        'views\manager.xml',
        'views\h_assistance.xml',
        'views\hostel_room_details.xml',
        'views\h_fees_management.xml',
        'wizard\h_fees_payment.xml',
    ],
    'depends': ['base', 'web','mail'],
    'installable': True,
    'license': 'LGPL-3',
}
