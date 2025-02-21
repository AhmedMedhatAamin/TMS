from odoo import models, fields
from datetime import timedelta

class DelayStopsWizard(models.TransientModel):
    _name = 'tms.delay.wizard'
    _description = 'Wizard to Delay Arrival and Departure Times for Stops'

    delay_minutes = fields.Integer(string="Posticipa (in minuti)", required=True)

    def apply_delay(self):
        stops = self.env['tms.stop'].browse(self._context.get('active_ids', []))
        for stop in stops:
            if stop.departure_time:
                stop.departure_time += timedelta(minutes=self.delay_minutes)
            if stop.arrival_time:
                stop.arrival_time += timedelta(minutes=self.delay_minutes)

        return {'type': 'ir.actions.act_window_close'}
