from odoo import http
from odoo.http import request

class BookingController(http.Controller):

    @http.route('/booking', type='http', auth='public', website=True)
    def booking_page(self):
        # Fetch predefined time slots from the Booking model
        predefined_times = request.env['elixir.booking'].PREDEFINED_TIMES

        # Fetch all wooden courts
        all_wooden_courts = request.env['elixir.badminton_court'].search([
            ('court_type', '=', 'wooden'),
        ])

        # Fetch all synthetic courts
        all_synthetic_courts = request.env['elixir.badminton_court'].search([
            ('court_type', '=', 'synthetic'),
        ])

        # Initialize dictionaries to store available time slots for wooden and synthetic courts
        available_time_slots_wooden = {time_slot[1]: [] for time_slot in predefined_times}
        available_time_slots_synthetic = {time_slot[1]: [] for time_slot in predefined_times}

        # Filter out booked courts for each predefined time slot
        for predefined_time in predefined_times:
            for wooden_court in all_wooden_courts:
                if not wooden_court.bookings.filtered(lambda b: b.predefined_time == predefined_time[0]):
                    available_time_slots_wooden[predefined_time[1]].append(wooden_court)

            for synthetic_court in all_synthetic_courts:
                if not synthetic_court.bookings.filtered(lambda b: b.predefined_time == predefined_time[0]):
                    available_time_slots_synthetic[predefined_time[1]].append(synthetic_court)

        # Filter out time slots with no available courts
        available_time_slots_wooden = {time_slot: courts for time_slot, courts in available_time_slots_wooden.items() if courts}
        available_time_slots_synthetic = {time_slot: courts for time_slot, courts in available_time_slots_synthetic.items() if courts}

        return request.render('elixir_sports_arena.available_booking_time_slots', {
            'available_time_slots_wooden': available_time_slots_wooden,
            'available_time_slots_synthetic': available_time_slots_synthetic,
        })

