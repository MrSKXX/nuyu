import requests
import json
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class WhatsAppConnector(models.Model):
    """
    WhatsApp Business API Connector
    Handles WhatsApp message sending, templates, and webhook processing
    Priority platform for Lebanese market communication
    """
    _name = 'social.whatsapp.connector'
    _description = 'WhatsApp Business API Connector'
    
    name = fields.Char(string='Connector Name', required=True, default='NuYu WhatsApp Business')
    platform_id = fields.Many2one('social.platform', string='Platform', required=True)
    
    # WhatsApp Business API Configuration
    access_token = fields.Char(string='Access Token', required=True, 
                              help="WhatsApp Business API Access Token")
    phone_number_id = fields.Char(string='Phone Number ID', required=True,
                                 help="WhatsApp Business Phone Number ID")
    business_phone = fields.Char(string='Business Phone Number', 
                                help="Format: +961XXXXXXXX (Lebanon)")
    webhook_verify_token = fields.Char(string='Webhook Verify Token')
    
    # API URLs
    api_base_url = fields.Char(string='API Base URL', 
                              default='https://graph.facebook.com/v18.0',
                              help="WhatsApp Business API base URL")
    
    # Lebanese Market Settings
    default_language = fields.Selection([
        ('en', 'English'),
        ('ar', 'Arabic')
    ], string='Default Language', default='en')
    
    timezone = fields.Selection([
        ('Asia/Beirut', 'Beirut Time (GMT+2/+3)'),
        ('UTC', 'UTC')
    ], string='Timezone', default='Asia/Beirut')
    
    # Status and Testing
    is_active = fields.Boolean(string='Active', default=True)
    connection_status = fields.Selection([
        ('disconnected', 'Disconnected'),
        ('connected', 'Connected'),
        ('error', 'Connection Error'),
        ('testing', 'Testing')
    ], string='Connection Status', default='disconnected')
    
    last_test_date = fields.Datetime(string='Last Test Date')
    last_error = fields.Text(string='Last Error Message')
    
    # Statistics
    messages_sent_today = fields.Integer(string='Messages Sent Today', default=0)
    messages_sent_total = fields.Integer(string='Total Messages Sent', default=0)
    success_rate = fields.Float(string='Success Rate %', default=0.0)
    
    def action_test_connection(self):
        """Test WhatsApp Business API connection"""
        self.connection_status = 'testing'
        
        try:
            # Test API connection by getting phone number info
            url = f"{self.api_base_url}/{self.phone_number_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.connection_status = 'connected'
                self.last_test_date = fields.Datetime.now()
                self.last_error = False
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('🟢 WhatsApp Connected!'),
                        'message': f'Successfully connected to WhatsApp Business: {data.get("display_phone_number", "Unknown")}',
                        'type': 'success'
                    }
                }
            else:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.connection_status = 'error'
            self.last_error = str(e)
            _logger.error(f"WhatsApp connection test failed: {e}")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('❌ WhatsApp Connection Failed'),
                    'message': f'Connection error: {str(e)[:100]}...',
                    'type': 'danger'
                }
            }
    
    def send_message(self, recipient_phone, message_content, message_type='text'):
        """
        Send WhatsApp message to recipient
        Main function for sending birthday campaigns and other messages
        """
        if not self.is_active or self.connection_status != 'connected':
            raise UserError(_('WhatsApp connector is not active or connected'))
        
        try:
            # Clean and format phone number for Lebanese market
            formatted_phone = self._format_lebanese_phone(recipient_phone)
            
            # Prepare message payload
            url = f"{self.api_base_url}/{self.phone_number_id}/messages"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'to': formatted_phone,
                'type': message_type,
                'text': {
                    'body': message_content
                }
            }
            
            # Send message
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                message_id = data.get('messages', [{}])[0].get('id')
                
                # Update statistics
                self.messages_sent_today += 1
                self.messages_sent_total += 1
                
                _logger.info(f"WhatsApp message sent successfully to {formatted_phone}, ID: {message_id}")
                return {
                    'success': True,
                    'message_id': message_id,
                    'recipient': formatted_phone
                }
            else:
                error_msg = f"WhatsApp API Error: {response.status_code} - {response.text}"
                _logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"WhatsApp send error: {str(e)}"
            _logger.error(error_msg)
            self.last_error = error_msg
            return {
                'success': False,
                'error': error_msg
            }
    
    def _format_lebanese_phone(self, phone):
        """
        Format phone number for Lebanese market
        Converts various formats to international format
        """
        if not phone:
            raise ValidationError(_('Phone number is required'))
        
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Lebanese number formatting
        if len(digits_only) == 8:
            # Local format (e.g., 81234567) -> +96181234567
            return f"961{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('961'):
            # Already has country code (96181234567) -> +96181234567
            return digits_only
        elif len(digits_only) == 12 and digits_only.startswith('+961'):
            # Already international format
            return digits_only[1:]  # Remove + for API
        elif len(digits_only) == 13 and digits_only.startswith('00961'):
            # International format with 00 prefix
            return digits_only[2:]  # Remove 00
        else:
            # Try to handle other formats or assume international
            if digits_only.startswith('961'):
                return digits_only
            else:
                raise ValidationError(f'Invalid Lebanese phone number format: {phone}')
    
    def send_birthday_campaign(self, campaign):
        """
        Send birthday campaign via WhatsApp
        Special handling for birthday messages with gender-specific content
        """
        if not campaign.message_ids:
            raise UserError(_('No messages found in campaign'))
        
        results = {
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        for message in campaign.message_ids:
            try:
                # Get recipient phone
                recipient = message.recipient_id
                if not recipient.phone and not recipient.mobile:
                    results['failed'] += 1
                    results['errors'].append(f'{recipient.name}: No phone number')
                    continue
                
                phone = recipient.mobile or recipient.phone
                
                # Send message
                result = self.send_message(phone, message.content)
                
                if result['success']:
                    # Update message status
                    message.write({
                        'state': 'sent',
                        'sent_date': fields.Datetime.now(),
                        'external_message_id': result.get('message_id')
                    })
                    results['sent'] += 1
                    
                    # Mark birthday campaign as sent for customer
                    if campaign.campaign_type == 'birthday':
                        recipient.write({
                            'birthday_campaign_sent': True,
                            'last_birthday_campaign': fields.Date.context_today(self)
                        })
                        
                else:
                    message.write({
                        'state': 'failed',
                        'error_message': result.get('error')
                    })
                    results['failed'] += 1
                    results['errors'].append(f'{recipient.name}: {result.get("error", "Unknown error")}')
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f'{message.recipient_id.name}: {str(e)}')
                _logger.error(f"Error sending WhatsApp message to {message.recipient_id.name}: {e}")
        
        return results
    
    def action_send_test_message(self):
        """Send test message to verify WhatsApp functionality"""
        if not self.business_phone:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('⚠️ Missing Phone Number'),
                    'message': 'Please add your business phone number first',
                    'type': 'warning'
                }
            }
        
        test_message = """🧪 NuYu WhatsApp Test Message 

مرحباً من نيويو سبا! 
Hello from NuYu Medical Spa!

This is a test message to verify WhatsApp Business API integration.

✅ If you receive this, the integration is working perfectly!

#NuYuSpa #WhatsAppTest"""
        
        try:
            result = self.send_message(self.business_phone, test_message)
            
            if result['success']:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('🧪 Test Message Sent!'),
                        'message': f'WhatsApp test sent to {self.business_phone}',
                        'type': 'success'
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('❌ Test Failed'),
                        'message': f'Error: {result.get("error", "Unknown error")}',
                        'type': 'danger'
                    }
                }
                
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('❌ Test Error'),
                    'message': f'Exception: {str(e)}',
                    'type': 'danger'
                }
            }
    
    @api.model
    def get_active_connector(self):
        """Get the active WhatsApp connector"""
        return self.search([('is_active', '=', True)], limit=1)
    
    def action_view_sent_messages(self):
        """View messages sent through this connector"""
        return {
            'name': f'WhatsApp Messages - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'social.message',
            'view_mode': 'tree,form',
            'domain': [('platform_id', '=', self.platform_id.id)],
            'context': {'default_platform_id': self.platform_id.id}
        }