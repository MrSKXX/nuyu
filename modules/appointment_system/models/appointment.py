# modules/appointment_system/models/appointment.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Appointment(models.Model):
    """
    Appointment Management - With Multiple Treatments
    """
    _name = 'appointment.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'
    
    name = fields.Char(string='Reference', required=True, default=lambda self: _('New'))
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    
    # Enhanced duration - computed from treatment lines
    duration = fields.Float(string='Total Duration (Hours)', compute='_compute_totals', store=True)
    
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, 
                                domain="[('is_company', '=', False)]")
    practitioner_id = fields.Many2one('res.users', string='Primary Practitioner', required=True)
    
    # Keep original treatment_type for backward compatibility and quick single treatments
    treatment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('botox', 'Botox'),
        ('filler', 'Filler'),
        ('facial', 'Facial'),
        ('laser', 'Laser'),
        ('other', 'Other'),
        ('multiple', 'Multiple Treatments')  # NEW option
    ], string='Treatment', required=True, default='consultation')
    
    room = fields.Char(string='Room')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    
    # Enhanced pricing - computed from treatment lines
    price = fields.Float(string='Total Price', compute='_compute_totals', store=True)
    
    # NEW: Treatment lines for multiple treatments
    treatment_line_ids = fields.One2many('appointment.treatment.line', 'appointment_id', string='Treatment Details')
    has_multiple_treatments = fields.Boolean(string='Multiple Treatments', compute='_compute_has_multiple')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('appointment.appointment') or _('New')
        return super().create(vals)
    
    @api.depends('treatment_line_ids.duration', 'treatment_line_ids.price')
    def _compute_totals(self):
        """Calculate totals from treatment lines"""
        for appointment in self:
            if appointment.treatment_line_ids:
                appointment.duration = sum(appointment.treatment_line_ids.mapped('duration'))
                appointment.price = sum(appointment.treatment_line_ids.mapped('price'))
            else:
                # Fallback to default values if no lines
                appointment.duration = 1.0
                appointment.price = 0.0
    
    @api.depends('treatment_line_ids')
    def _compute_has_multiple(self):
        """Check if appointment has multiple treatments"""
        for appointment in self:
            appointment.has_multiple_treatments = len(appointment.treatment_line_ids) > 1
    
    @api.onchange('treatment_type')
    def _onchange_treatment_type(self):
        """Auto-create treatment line when single treatment is selected"""
        if self.treatment_type and self.treatment_type != 'multiple':
            # Clear existing lines if switching from multiple to single
            if len(self.treatment_line_ids) > 1:
                self.treatment_line_ids = [(5, 0, 0)]  # Clear all
            
            # Create or update single treatment line
            if not self.treatment_line_ids:
                self.treatment_line_ids = [(0, 0, {
                    'treatment_type': self.treatment_type,
                    'practitioner_id': self.practitioner_id.id,
                })]
            else:
                # Update existing line
                self.treatment_line_ids[0].treatment_type = self.treatment_type
    
    def action_confirm(self):
        if not self.treatment_line_ids:
            # Auto-create line for single treatments
            if self.treatment_type != 'multiple':
                self.treatment_line_ids = [(0, 0, {
                    'treatment_type': self.treatment_type,
                    'practitioner_id': self.practitioner_id.id,
                })]
            else:
                raise ValidationError("Please add treatment details before confirming.")
        self.state = 'confirmed'
        
    def action_done(self):
        self.state = 'done'
        
    def action_cancel(self):
        self.state = 'cancelled'


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
    
    # Practitioner who performs this specific treatment (for commission tracking)
    practitioner_id = fields.Many2one('res.users', string='Practitioner')
    
    duration = fields.Float(string='Duration (Hours)', default=1.0)
    price = fields.Float(string='Price')
    
    notes = fields.Text(string='Treatment Notes')
    
    @api.onchange('treatment_type')
    def _onchange_treatment_type(self):
        """Set default duration and price based on treatment"""
        defaults = {
            'consultation': {'duration': 0.5, 'price': 50.0},
            'botox': {'duration': 1.0, 'price': 300.0},
            'filler': {'duration': 1.5, 'price': 400.0},
            'hydrafacial': {'duration': 1.0, 'price': 150.0},
            'coolsculpting': {'duration': 2.0, 'price': 800.0},
            'laser': {'duration': 0.75, 'price': 200.0},
            'facial': {'duration': 1.0, 'price': 100.0},
            'red_light': {'duration': 0.5, 'price': 75.0},
            'chemical_peel': {'duration': 0.75, 'price': 120.0},
            'microneedling': {'duration': 1.0, 'price': 180.0},
            'other': {'duration': 1.0, 'price': 0.0}
        }
        
        if self.treatment_type and self.treatment_type in defaults:
            values = defaults[self.treatment_type]
            self.duration = values['duration']
            self.price = values['price']