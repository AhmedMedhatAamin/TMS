from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    default_trip_type_id = fields.Many2one('tms.trip.type', string="Default Trip Type")