# modules/appointment_system/models/appointment.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Appointment(models.Model):
    """
    Enhanced Appointment Management - Calendar UI Style
    """
    _name = 'appointment.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'
    
    name = fields.Char(string='Reference', required=True, default=lambda self: _('New'))
    appointment_date = fields.Datetime(string='Date and Time', required=True, tracking=True)
    
    # Computed end date for calendar view
    appointment_end_date = fields.Datetime(string='End Date', compute='_compute_end_date', store=True)
    all_day = fields.Boolean(string='All Day', default=False)
    
    # Duration fields - FIXED: Use string values instead of integers
    duration = fields.Float(string='Duration (Minutes)', default=15.0)
    duration_selection = fields.Selection([
        ('15', '15 min'),
        ('30', '30 min'),
        ('45', '45 min'),
        ('60', '1 hour'),
        ('90', '1.5 hours'),
        ('120', '2 hours'),
        ('150', '2.5 hours'),
        ('180', '3 hours')
    ], string='Duration', default='15')
    
    # Patient information
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, 
                                domain="[('is_company', '=', False)]", tracking=True)
    
    # Department selection matching the UI
    department = fields.Selection([
        ('verdun', 'Verdun'),
        ('achrafieh', 'Achrafieh'),
        ('beirut_central', 'Beirut Central'),
        ('dbayeh', 'Dbayeh')
    ], string='Department', default='verdun')
    
    # Staff assignments
    practitioner_id = fields.Many2one('res.users', string='Specialist', required=True, tracking=True)
    assistant_id = fields.Many2one('res.users', string='Assistant', domain="[('share', '=', False)]")
    
    # Category selection
    category = fields.Selection([
        ('aesthetic', 'Aesthetic Treatment'),
        ('medical', 'Medical Treatment'),
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow Up'),
        ('emergency', 'Emergency')
    ], string='Category')
    
    # Service/Treatment type
    treatment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('botox', 'Botox'),
        ('filler', 'Dermal Fillers'),
        ('facial', 'Facial Treatment'),
        ('laser', 'Laser Treatment'),
        ('hydrafacial', 'HydraFacial'),
        ('coolsculpting', 'CoolSculpting'),
        ('red_light', 'Red Light Therapy'),
        ('chemical_peel', 'Chemical Peel'),
        ('microneedling', 'Microneedling'),
        ('iv_therapy', 'IV Therapy'),
        ('massage', 'Massage Therapy'),
        ('other', 'Other Service')
    ], string='Service', required=True, default='consultation', tracking=True)
    
    # Equipment and location
    machine = fields.Selection([
        ('none', 'No Machine Required'),
        ('laser_co2', 'CO2 Laser'),
        ('hydrafacial_machine', 'HydraFacial Machine'),
        ('coolsculpting_machine', 'CoolSculpting'),
        ('ipl_machine', 'IPL Machine'),
        ('rf_microneedling', 'RF Microneedling'),
        ('diode_laser', 'Diode Laser'),
        ('nd_yag_laser', 'Nd:YAG Laser')
    ], string='Machine', default='none')
    
    room = fields.Selection([
        ('room_1', 'Treatment Room 1'),
        ('room_2', 'Treatment Room 2'),
        ('room_3', 'Treatment Room 3'),
        ('consultation_room', 'Consultation Room'),
        ('laser_room', 'Laser Room'),
        ('procedure_room', 'Procedure Room'),
        ('vip_room', 'VIP Room')
    ], string='Room')
    
    # Case type
    case_type = fields.Selection([
        ('new_case', 'New Case'),
        ('follow_up', 'Follow Up Case'),
        ('touch_up', 'Touch Up'),
        ('maintenance', 'Maintenance'),
        ('emergency', 'Emergency Case'),
        ('consultation_only', 'Consultation Only')
    ], string='Case')
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ], string='Status', default='draft', tracking=True)
    
    # Notes and descriptions
    notes = fields.Text(string='Description')
    reminder_notes = fields.Text(string='Reminder')
    
    # Pricing
    price = fields.Float(string='Price', default=0.0)
    
    # Checkbox fields
    new_patient = fields.Boolean(string='New Patient', default=False)
    call_back = fields.Boolean(string='Call Back', default=False)
    private = fields.Boolean(string='Private', default=False)
    notifications = fields.Boolean(string='Notifications', default=True)
    
    # Notification settings
    notification_sms = fields.Boolean(string='SMS', default=True)
    notification_email = fields.Boolean(string='Email', default=False)
    notification_language = fields.Selection([
        ('arabic', 'Arabic'),
        ('english', 'English'),
        ('french', 'French')
    ], string='Language', default='english')
    
    notification_timing = fields.Selection([
        ('now', 'Now'),
        ('2_hours', '2 Hours Earlier'),
        ('1_day', '1 Day Earlier'),
        ('2_days', '2 Days Earlier'),
        ('3_days', '3 Days Earlier'),
        ('1_week', '1 Week Earlier')
    ], string='When?', default='1_day')
    
    # Multiple treatments support
    treatment_line_ids = fields.One2many('appointment.treatment.line', 'appointment_id', string='Treatment Details')
    has_multiple_treatments = fields.Boolean(string='Multiple Treatments', compute='_compute_has_multiple')
    
    # Patient contact info
    patient_phone = fields.Char(related='patient_id.phone', string='Phone', readonly=True)
    patient_email = fields.Char(related='patient_id.email', string='Email', readonly=True)
    
    # Calendar display
    display_name_calendar = fields.Char(string='Calendar Display', compute='_compute_calendar_display')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('appointment.appointment') or _('New')
        return super().create(vals)
    
    @api.depends('appointment_date', 'duration_selection', 'duration', 'all_day')
    def _compute_end_date(self):
        """Calculate end date for calendar view"""
        for appointment in self:
            if appointment.appointment_date:
                if appointment.all_day:
                    appointment.appointment_end_date = appointment.appointment_date
                else:
                    # Convert duration_selection string to float
                    duration_minutes = float(appointment.duration_selection) if appointment.duration_selection else appointment.duration or 15
                    appointment.appointment_end_date = appointment.appointment_date + timedelta(minutes=duration_minutes)
            else:
                appointment.appointment_end_date = False
    
    @api.depends('patient_id', 'treatment_type', 'room', 'appointment_date')
    def _compute_calendar_display(self):
        """Generate display name for calendar"""
        for appointment in self:
            parts = []
            if appointment.patient_id:
                parts.append(appointment.patient_id.name)
            if appointment.treatment_type:
                treatment_name = dict(appointment._fields['treatment_type'].selection).get(appointment.treatment_type, '')
                parts.append(f"({treatment_name})")
            if appointment.room:
                room_name = dict(appointment._fields['room'].selection).get(appointment.room, appointment.room)
                parts.append(room_name)
            appointment.display_name_calendar = ' - '.join(parts) if parts else 'New Appointment'
    
    @api.depends('treatment_line_ids')
    def _compute_has_multiple(self):
        """Check if appointment has multiple treatments"""
        for appointment in self:
            appointment.has_multiple_treatments = len(appointment.treatment_line_ids) > 1
    
    @api.onchange('duration_selection')
    def _onchange_duration_selection(self):
        """Update duration field when selection changes"""
        if self.duration_selection:
            self.duration = float(self.duration_selection)
    
    @api.onchange('treatment_type')
    def _onchange_treatment_type(self):
        """Set default duration and price based on treatment"""
        if self.treatment_type and self.treatment_type != 'multiple':
            defaults = {
                'consultation': {'duration': '30', 'price': 75.0},
                'botox': {'duration': '45', 'price': 400.0},
                'filler': {'duration': '60', 'price': 500.0},
                'hydrafacial': {'duration': '60', 'price': 200.0},
                'coolsculpting': {'duration': '120', 'price': 1200.0},
                'laser': {'duration': '30', 'price': 250.0},
                'facial': {'duration': '90', 'price': 150.0},
                'red_light': {'duration': '30', 'price': 100.0},
                'chemical_peel': {'duration': '45', 'price': 180.0},
                'microneedling': {'duration': '60', 'price': 250.0},
                'iv_therapy': {'duration': '45', 'price': 120.0},
                'massage': {'duration': '60', 'price': 100.0},
                'other': {'duration': '30', 'price': 0.0}
            }
            
            if self.treatment_type in defaults:
                values = defaults[self.treatment_type]
                self.duration_selection = values['duration']
                self.duration = float(values['duration'])
                self.price = values['price']
    
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Auto-check new patient if no previous appointments"""
        if self.patient_id:
            # Only search if we have a real ID (not for new records)
            if self.id and not isinstance(self.id, models.NewId):
                existing_appointments = self.search([
                    ('patient_id', '=', self.patient_id.id),
                    ('id', '!=', self.id)
                ], limit=1)
                self.new_patient = not bool(existing_appointments)
            else:
                # For new records, check if any appointments exist for this patient
                existing_appointments = self.search([
                    ('patient_id', '=', self.patient_id.id)
                ], limit=1)
                self.new_patient = not bool(existing_appointments)
    
    def action_confirm(self):
        """Confirm appointment"""
        self.state = 'confirmed'
        self._create_calendar_event()
        return {'type': 'ir.actions.act_window_close'}
        
    def action_done(self):
        """Mark appointment as completed"""
        self.state = 'done'
        
    def action_cancel(self):
        """Cancel appointment"""
        self.state = 'cancelled'
        
    def _create_calendar_event(self):
        """Create calendar event for the practitioner"""
        self.ensure_one()
        if self.practitioner_id and self.state == 'confirmed':
            event_vals = {
                'name': f"{self.patient_id.name} - {self.treatment_type.title()}",
                'start': self.appointment_date,
                'stop': self.appointment_end_date,
                'user_id': self.practitioner_id.id,
                'partner_ids': [(6, 0, [self.patient_id.id])],
                'description': f"Patient: {self.patient_id.name}\n"
                             f"Service: {dict(self._fields['treatment_type'].selection).get(self.treatment_type)}\n"
                             f"Department: {dict(self._fields['department'].selection).get(self.department) if self.department else 'N/A'}\n"
                             f"Room: {dict(self._fields['room'].selection).get(self.room) if self.room else 'TBD'}\n"
                             f"Duration: {self.duration_selection} minutes\n"
                             f"Notes: {self.notes or ''}",
                'location': f"{self.department} - {self.room}" if self.department and self.room else self.room or self.department,
            }
            try:
                self.env['calendar.event'].create(event_vals)
            except Exception:
                # If calendar creation fails, don't break the appointment creation
                pass


class AppointmentTreatmentLine(models.Model):
    """
    Treatment Lines for Multi-Treatment Appointments
    """
    _name = 'appointment.treatment.line'
    _description = 'Appointment Treatment Line'
    _order = 'sequence, id'
    
    appointment_id = fields.Many2one('appointment.appointment', string='Appointment', ondelete='cascade')
    sequence = fields.Integer(string='Order', default=10)
    
    treatment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('botox', 'Botox Treatment'),
        ('filler', 'Dermal Fillers'),
        ('hydrafacial', 'HydraFacial'),
        ('coolsculpting', 'CoolSculpting'),
        ('laser', 'Laser Treatment'),
        ('facial', 'Facial Treatment'),
        ('red_light', 'Red Light Therapy'),
        ('chemical_peel', 'Chemical Peel'),
        ('microneedling', 'Microneedling'),
        ('other', 'Other Treatment')
    ], string='Treatment', required=True)
    
    practitioner_id = fields.Many2one('res.users', string='Practitioner')
    duration = fields.Float(string='Duration (Minutes)', default=30.0)
    price = fields.Float(string='Price')
    notes = fields.Text(string='Treatment Notes')
    
    @api.onchange('treatment_type')
    def _onchange_treatment_type(self):
        """Set default duration and price based on treatment"""
        defaults = {
            'consultation': {'duration': 30, 'price': 75.0},
            'botox': {'duration': 45, 'price': 400.0},
            'filler': {'duration': 60, 'price': 500.0},
            'hydrafacial': {'duration': 60, 'price': 200.0},
            'coolsculpting': {'duration': 120, 'price': 1200.0},
            'laser': {'duration': 30, 'price': 250.0},
            'facial': {'duration': 90, 'price': 150.0},
            'red_light': {'duration': 30, 'price': 100.0},
            'chemical_peel': {'duration': 45, 'price': 180.0},
            'microneedling': {'duration': 60, 'price': 250.0},
            'other': {'duration': 30, 'price': 0.0}
        }
        
        if self.treatment_type and self.treatment_type in defaults:
            values = defaults[self.treatment_type]
            self.duration = values['duration']
            self.price = values['price']