from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Related to the company's default trip type
    default_trip_type_id = fields.Many2one(
        'tms.trip.type',
        string="Default Trip Type",
        related='company_id.default_trip_type_id',
        readonly=False,
        default_model='tms.trip'
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            default_trip_type_id=self.env.company.default_trip_type_id.id,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env.company.default_trip_type_id = self.default_trip_type_id