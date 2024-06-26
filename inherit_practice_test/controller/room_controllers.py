from odoo import http,_
from odoo.http import request
from odoo.exceptions import ValidationError


class HostelRoomController(http.Controller):

    @http.route('/hostel/available_rooms', type='http', auth='public', website=True)
    def available_rooms(self):
        # Fetch available rooms
        available_rooms = request.env['hostel.room'].search([('availability', '=', True)])

        # Check if any rooms are available
        if not available_rooms:
            raise ValidationError(_("No rooms are currently available for booking."))

        # Render template with available rooms
        return request.render('your_module.available_rooms_template', {
            'available_rooms': available_rooms,
        })
