from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    trip_ids = fields.One2many('tms.trip', 'customer_id', string='Trips')
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
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }