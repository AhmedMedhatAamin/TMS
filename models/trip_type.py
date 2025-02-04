from odoo import models, fields, api

class TMSTripType(models.Model):
    _name = 'tms.trip.type'
    _description = 'Trip Type'

    name = fields.Char(string='Name')
    trip_ids = fields.One2many('tms.trip', 'trip_type_id', string='Trips')
    trip_count = fields.Integer(string="Trip Count", compute='_compute_trip_count', store=True)

    @api.depends('trip_ids')
    def _compute_trip_count(self):
        for record in self:
            record.trip_count = len(record.trip_ids)

   
    def action_view_trips(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trips',
            'res_model': 'tms.trip',
            'view_mode': 'list,form',
            'domain': [('trip_type_id', '=', self.id)],
            'context': {'default_trip_type_id': self.id},
        }