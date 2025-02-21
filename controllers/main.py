from odoo import http
from odoo.http import request

class TripController(http.Controller):

    # Route to display a list of trips for selection
    @http.route('/trip/select', type='http', auth='public', website=True)
    def trip_select(self, **kwargs):
        trips = request.env['tms.trip'].sudo().search([])
        if not trips:
            return request.not_found()
        return request.render('soa1_ahmed_tms.trip_select_template', {'trips': trips})

    # Route to display the details of a specific trip
    @http.route('/trip/info/<int:trip_id>', type='http', auth='public', website=True)
    def trip_info(self, trip_id, **kwargs):
        trip = request.env['tms.trip'].sudo().browse(trip_id)
        if not trip.exists():
            return request.not_found()
        return request.render('soa1_ahmed_tms.trip_template', {'trip': trip})

    # Route to update the trip name
    @http.route('/trip/update_name', type='http', auth='public', methods=['POST'], csrf=False)
    def update_trip_name(self, **post):
        try:
            trip_id = int(post.get("trip_id"))
            trip_name = post.get("trip_name")
            
            # Ensure trip exists before writing
            trip = request.env['tms.trip'].sudo().browse(trip_id)
            if trip.exists():
                trip.sudo().write({'name': trip_name})
                return """
                    <html>
                        <head><title>Updated Trip Name</title></head>
                        <body>
                            <h2>Trip Name Updated!</h2>
                            <p><a href='/trip/info/{}'>Return to Trip</a></p>
                        </body>
                    </html>
                """.format(trip_id)
            else:
                return request.not_found()
        except Exception as e:
            return f"""
            <html>
                <body>
                    <h2>Error Updating Trip</h2>
                    <p>{str(e)}</p>
                </body>
            </html>
            """