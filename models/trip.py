from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

class Trip(models.Model):
    _name = 'tms.trip'
    _description = 'Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', default='New')
    trip_type_id = fields.Many2one(
        'tms.trip.type', 
        string='Trip Type',
        default=lambda self: self.env.company.default_trip_type_id.id,
        required=True
    )
    customer_id = fields.Many2one('res.partner', string='Customer')
    stop_ids = fields.One2many('tms.stop', 'trip_id', string="Stops")
    stop_count = fields.Integer(string="Stop Count", compute='_compute_stop_count', store=False)
    location_id = fields.Many2one('res.partner', string="Departure Location", store=True, compute='_compute_departure', inverse='_set_departure')
    arrival = fields.Many2one('res.partner', string="Arrival Location", store=True, compute='_compute_arrival', inverse='_set_arrival')
    arrival_date = fields.Datetime(string="Arrival Date", compute='_compute_arrival_date', inverse='_set_arrival_date', store=True)
    departure_date = fields.Datetime(string="Departure Date", compute='_compute_departure_date', inverse='_set_departure_date', store=True)
    all_stops_for_partner = fields.Many2many('tms.stop', string="All Stops for Partner", compute='_compute_all_stops_for_partner', store=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    note = fields.Text(string="Trip Summary", store=True, compute="_compute_trip_note", readonly=False)

    unique_stops_with_partners = fields.Many2many(
        'res.partner',
        string="Unique Stops",
        compute='_compute_unique_stops_with_partners',
        store=False
    )

    unique_stops_with_partners_italia = fields.Many2many(
        'res.partner',
        string="Unique Italian Partners",
        compute='_compute_unique_stops_with_partners_italia',
        store=False
    )

    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string="State", default="planned")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('company_id'):
                vals['company_id'] = self.env.company.id
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tms.trip') or 'New'
        return super(Trip, self).create(vals_list)

    @api.constrains('company_id')
    def _check_company(self):
        for trip in self:
            if trip.company_id != self.env.company:
                raise AccessError("The trip does not belong to your company.")
            
    @api.depends('stop_ids')
    def _compute_stop_count(self):
        for trip in self:
            trip.stop_count = len(trip.stop_ids)

    def _update_first_or_last_stop(self, field_name, attr_name):
        for trip in self:
            if trip.stop_ids:
                stop = trip.stop_ids[0] if field_name in ['location_id', 'departure_date'] else trip.stop_ids[-1]
                if getattr(trip, field_name):
                    setattr(stop, attr_name, getattr(trip, field_name))

    @api.depends('stop_ids')
    def _compute_departure(self):
        self._update_first_or_last_stop('location_id', 'stops_location_id')

    @api.depends('stop_ids')
    def _compute_arrival(self):
        self._update_first_or_last_stop('arrival', 'stops_location_id')

    def _set_departure(self):
        self._update_first_or_last_stop('location_id', 'stops_location_id')

    def _set_arrival(self):
        self._update_first_or_last_stop('arrival', 'stops_location_id')

    @api.depends('stop_ids')
    def _compute_arrival_date(self):
        self._update_first_or_last_stop('arrival_date', 'arrival_time')

    @api.depends('stop_ids')
    def _compute_departure_date(self):
        self._update_first_or_last_stop('departure_date', 'departure_time')

    def _set_arrival_date(self):
        self._update_first_or_last_stop('arrival_date', 'arrival_time')

    def _set_departure_date(self):
        self._update_first_or_last_stop('departure_date', 'departure_time')

    @api.constrains('departure_date', 'arrival_date')
    def _check_dates(self):
        for trip in self:
            if trip.departure_date and trip.arrival_date and trip.departure_date > trip.arrival_date:
                raise ValidationError("Departure date must be before arrival date.")

    @api.onchange('location_id')
    def _onchange_location_id(self):
        """ Updates the first stop location when the departure location is changed. """
        self._update_first_or_last_stop('location_id', 'stops_location_id')

    @api.onchange('arrival')
    def _onchange_arrival(self):
        """ Updates the last stop location when the arrival location is changed. """
        self._update_first_or_last_stop('arrival', 'stops_location_id')

    def action_view_stops(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Stops",
            "res_model": "tms.stop",
            "view_mode": "tree,form",
            "domain": [("trip_id", "=", self.id)],
        }

    def action_start_trip(self):
        for trip in self:
            if trip.state == 'planned':
                trip.state = 'in_progress'

    def action_complete_trip(self):
        for trip in self:
            if trip.state == 'in_progress':
                trip.state = 'completed'

    def action_say_ciao(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Ciao!',
                'message': f'Seleziona il tuo viaggio {self.name}!' if self.name else 'Seleziona il tuo viaggio!',
                'sticky': False,
            }
        }
    
    def open_trip_info(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': 'View Trip Info',
            'url': f'/trip/info/{self.id}',
            'target': 'new',
        }

    @api.depends('location_id', 'arrival', 'departure_date', 'arrival_date')
    def _compute_trip_note(self):
        for trip in self:
            if trip.location_id and trip.arrival and trip.departure_date and trip.arrival_date:
                departure = trip.location_id.name
                arrival = trip.arrival.name
                departure_date = trip.departure_date.strftime('%Y-%m-%d %H:%M')
                arrival_date = trip.arrival_date.strftime('%Y-%m-%d %H:%M')
                trip.note = f"The customer will leave from {departure} on {departure_date} and arrive at {arrival} on {arrival_date}."
            else:
                trip.note = ""

    @api.onchange('location_id', 'arrival', 'departure_date', 'arrival_date')
    def _onchange_trip_details(self):
        """ Ensure the note is updated when trip details change. """
        self._compute_trip_note()

    @api.depends('stop_ids.stops_location_id')
    def _compute_unique_stops_with_partners_italia(self):
        for trip in self:
            # Filter only partners with country 'Italy'
            italian_partners = trip.stop_ids.mapped('stops_location_id').filtered(lambda p: p.country_id and p.country_id.name == 'Italy')
            trip.unique_stops_with_partners_italia = [(6, 0, italian_partners.ids)]

    @api.depends('stop_ids.stops_location_id')
    def _compute_unique_stops_with_partners(self):
        for trip in self:
            # Extract unique partner IDs from stops
            trip.unique_stops_with_partners = [(6, 0, trip.stop_ids.mapped('stops_location_id').ids)]