from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Stop(models.Model):
    _name = 'tms.stop'
    _description = 'Stop'
    _order = 'departure_time asc'

    name = fields.Char(string='Name')
    sequence = fields.Integer(string="Sequence", default=10)
    stops_location_id = fields.Many2one('res.partner', string="Stops")
    departure_time = fields.Datetime(string="Departure Time")
    arrival_time = fields.Datetime(string="Arrival Time")
    trip_id = fields.Many2one('tms.trip', string="Trip")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
                
    @api.constrains('departure_time', 'arrival_time')
    def _check_departure_arrival(self):
        for stop in self.filtered(lambda s: s.departure_time or s.arrival_time):
            if stop.departure_time and stop.arrival_time:
                if stop.departure_time > stop.arrival_time:
                    raise ValidationError("La data di partenza non può essere successiva alla data di arrivo.")
