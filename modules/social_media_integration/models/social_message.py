from odoo import models, fields, api, _
from datetime import datetime

class SocialMessage(models.Model):
    _name = 'social.message'
    _description = 'Social Media Message'
    _order = 'create_date desc'
    
    name = fields.Char(string='Message Reference', compute='_compute_name', store=True)
    
    campaign_id = fields.Many2one('social.campaign', string='Campaign')
    recipient_id = fields.Many2one('res.partner', string='Recipient', required=True)
    platform_id = fields.Many2one('social.platform', string='Platform', required=True)
    
    content = fields.Text(string='Message Content', required=True)
    media_url = fields.Char(string='Media URL')
    has_media = fields.Boolean(string='Has Media')
    
    scheduled_date = fields.Datetime(string='Scheduled Date', default=fields.Datetime.now)
    sent_date = fields.Datetime(string='Sent Date')
    delivered_date = fields.Datetime(string='Delivered Date')
    read_date = fields.Datetime(string='Read Date')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
        ('replied', 'Replied')
    ], string='Status', default='draft')
    
    has_response = fields.Boolean(string='Has Response', default=False)
    response_content = fields.Text(string='Response Content')
    response_date = fields.Datetime(string='Response Date')
    is_appointment_inquiry = fields.Boolean(string='Appointment Inquiry', default=False)
    
    external_message_id = fields.Char(string='External Message ID')
    webhook_response = fields.Text(string='Webhook Response')
    
    # Add missing fields
    error_message = fields.Text(string='Error Message')
    retry_count = fields.Integer(string='Retry Count', default=0)
    max_retries = fields.Integer(string='Max Retries', default=3)
    
    @api.depends('recipient_id', 'platform_id', 'create_date')
    def _compute_name(self):
        for message in self:
            if message.recipient_id and message.platform_id:
                message.name = f"{message.platform_id.platform_type.title()} to {message.recipient_id.name}"
            else:
                message.name = f"Message {message.id}"
    
    def action_send_now(self):
        """Send message immediately using appropriate platform"""
        if self.state not in ['draft', 'scheduled', 'failed']:
            return
        
        self.state = 'sending'
        
        if self.platform_id.platform_type == 'whatsapp':
            success = self._send_whatsapp_message()
        elif self.platform_id.platform_type == 'email':
            success = self._send_email_message()
        else:
            # For demo platforms, just mark as sent
            success = True
            self.external_message_id = f"demo_{self.platform_id.platform_type}_{self.id}"
        
        if success:
            self.sent_date = fields.Datetime.now()
            self.state = 'sent'
        else:
            self.state = 'failed'
            self.retry_count += 1
    
    def _send_whatsapp_message(self):
        """Send message via WhatsApp (demo mode for now)"""
        try:
            # For demo mode, just simulate sending
            if not self.platform_id.api_token or self.platform_id.api_token == 'demo_token_123':
                # Demo mode - simulate successful send
                self.external_message_id = f"demo_wa_{self.id}_{datetime.now().timestamp()}"
                return True
            
            # Real WhatsApp API would go here
            # For now, simulate success
            self.external_message_id = f"wa_{self.id}_{datetime.now().timestamp()}"
            return True
            
        except Exception as e:
            self.error_message = f"WhatsApp send error: {str(e)}"
            return False
    
    def _send_email_message(self):
        """Send message via email"""
        if not self.recipient_id.email:
            self.error_message = "Recipient has no email address"
            return False
        
        try:
            mail_values = {
                'subject': f'NuYu Medical Spa - {self.campaign_id.name if self.campaign_id else "Message"}',
                'body_html': self.content,
                'email_to': self.recipient_id.email,
                'email_from': self.env.company.email,
            }
            
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
            self.external_message_id = f"email_{mail.id}"
            return True
        except Exception as e:
            self.error_message = str(e)
            return False