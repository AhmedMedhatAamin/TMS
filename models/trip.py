from odoo import models, fields, api

class Trip(models.Model):
    _name = 'tms.trip'
    _description = 'Trip'

    name = fields.Char(string="Name")
    trip_type_id = fields.Many2one('tms.trip.type', string="Trip Type")
    customer_id = fields.Many2one('res.partner', string='Customer')
    stop_ids = fields.One2many('tms.stop', 'trip_id', string="Stops")
    stop_count = fields.Integer(string="Stop Count", compute='_compute_stop_count')

    @api.depends('stop_ids')
    def _compute_stop_count(self):
        for trip in self:
            trip.stop_count = len(trip.stop_ids)

    def action_view_stops(self):
          return {
            "type": "ir.actions.act_window",
            "name": "Stops",
            "res_model": "tms.stop",
            "view_mode": "list,form",
            "domain": [("trip_id", "=", self.id)],
        }