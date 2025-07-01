from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Appointment(models.Model):
    """
    Appointment Management
    """
    _name = 'appointment.appointment'
    _description = 'Medical Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'appointment_date desc'
    
    name = fields.Char(string='Reference', required=True, default=lambda self: _('New'))
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    duration = fields.Float(string='Duration (Hours)', default=1.0)
    
    patient_id = fields.Many2one('res.partner', string='Patient', required=True, 
                                domain="[('is_company', '=', False)]")
    practitioner_id = fields.Many2one('res.users', string='Practitioner', required=True)
    
    treatment_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('botox', 'Botox'),
        ('filler', 'Filler'),
        ('facial', 'Facial'),
        ('laser', 'Laser'),
        ('other', 'Other')
    ], string='Treatment', required=True, default='consultation')
    
    room = fields.Char(string='Room')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    price = fields.Float(string='Price')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('appointment.appointment') or _('New')
        return super().create(vals)
    
    def action_confirm(self):
        self.state = 'confirmed'
        
    def action_done(self):
        self.state = 'done'
        
    def action_cancel(self):
        self.state = 'cancelled'