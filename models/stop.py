from odoo import models, fields

class TmsStop(models.Model):
    _name = 'tms.stop'
    _description = 'TMS Stop'

    name = fields.Char(string="Stop Name", required=True)
    trip_id = fields.Many2one('tms.trip', string='Trip')
    departure_time = fields.Datetime(string='Departure Time')
    arrival_time = fields.Datetime(string='Arrival Time')
    stop_address_id = fields.Many2one(
        'res.partner',
        string="Indirizzo dello Stop",
        domain=[('type', '=', 'delivery')],
        help="Select the stop address from contacts that are marked as 'Delivery Address'."
    )

    def action_view_stops(self):
          return {
            "type": "ir.actions.act_window",
            "name": "Stops",
            "res_model": "tms.stop",
            "view_mode": "list,form",
            "domain": [("trip_id", "=", self.id)],
        }