from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TMSTripType(models.Model):
    _name = 'tms.trip.type'
    _description = 'Trip Type'

    name = fields.Char(string='Name')
    trip_ids = fields.One2many('tms.trip', 'trip_type_id', string='Trips')
    trip_type_id = fields.Many2one('tms.trip.type', string='Parent Trip Type')
    trip_count = fields.Integer(string="Trip Count", compute='_compute_trip_count', store=True)
    has_trips = fields.Boolean(string="Has Trips", compute='_compute_has_trips')
    color = fields.Integer()
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('trip_ids')
    def _compute_trip_count(self):
        for record in self:
            record.trip_count = len(record.trip_ids)
    
    @api.depends('trip_count')
    def _compute_has_trips(self):
        for record in self:
            record.has_trips = record.trip_count > 0
            
    def action_view_trips(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trips',
            'res_model': 'tms.trip',
            'view_mode': 'tree,form',
            'domain': [('trip_type_id', '=', self.id)],
            'context': {'default_trip_type_id': self.id},
        }

    def action_open_trips(self):
        """ Opens a list of trips related to this trip type. """
        return {
            'name': 'Trips',
            'type': 'ir.actions.act_window',
            'res_model': 'tms.trip',
            'view_mode': 'tree,form',
            'domain': [('trip_type_id', '=', self.id)],
            'target': 'current',
        }
    def action_form_trip(self):
        return {
            "type": "ir.actions.act_window",
            "name": "New Trip",
            "res_model": "tms.trip",
            "view_mode": "form",
            "target": "current",
            "context": {"default_trip_type_id": self.id},
        }
    def action_view_planned_trips(self):
        """ Action to view planned trips. """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Planned Trips',
            'res_model': 'tms.trip',
            'view_mode': 'tree,form',
            'domain': [('trip_type_id', '=', self.id), ('state', '=', 'planned')],
            'context': {'default_trip_type_id': self.id},
        }

    def action_view_in_progress_trips(self):
        """ Action to view trips in progress. """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trips in Progress',
            'res_model': 'tms.trip',
            'view_mode': 'tree,form',
            'domain': [('trip_type_id', '=', self.id), ('state', '=', 'in_progress')],
            'context': {'default_trip_type_id': self.id},
        }

    def action_view_completed_trips(self):
        """ Action to view completed trips. """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Completed Trips',
            'res_model': 'tms.trip',
            'view_mode': 'tree,form',
            'domain': [('trip_type_id', '=', self.id), ('state', '=', 'completed')],
            'context': {'default_trip_type_id': self.id},
        }
    
