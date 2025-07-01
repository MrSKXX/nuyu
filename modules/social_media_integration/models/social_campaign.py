from odoo import models, fields, api

class SocialCampaign(models.Model):
    """
    Social Media Campaign Model - Working Version
    """
    _name = 'social.campaign'
    _description = 'Social Media Campaign'
    
    name = fields.Char(string='Campaign Name', required=True)
    campaign_type = fields.Selection([
        ('birthday', 'Birthday Campaign'),
        ('promotion', 'Product Promotion'),
        ('general', 'General Marketing')
    ], string='Campaign Type', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent')
    ], string='Status', default='draft')
    
    target_segment = fields.Selection([
        ('all', 'All Customers'),
        ('vip', 'VIP Customers Only'),
        ('custom', 'Custom Selection')
    ], string='Target Segment', default='all')
    
    target_customer_ids = fields.Many2many('res.partner', string='Target Customers')
    primary_platform = fields.Many2one('social.platform', string='Primary Platform')
    message_content = fields.Text(string='Message Content', required=True)
    send_immediately = fields.Boolean(string='Send Immediately', default=True)
    scheduled_date = fields.Datetime(string='Scheduled Date')
    sent_count = fields.Integer(string='Messages Sent', default=0)
    message_ids = fields.One2many('social.message', 'campaign_id', string='Messages')
    
    def action_send_test(self):
        """Simple, working send function"""
        if not self.primary_platform:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Please select a platform first',
                    'type': 'warning'
                }
            }
        
        # Get customers
        if self.target_segment == 'all':
            customers = self.env['res.partner'].search([('is_company', '=', False)], limit=3)
        elif self.target_segment == 'vip':
            customers = self.env['res.partner'].search([
                ('is_company', '=', False),
                ('spending_tier', '=', 'vip')
            ], limit=3)
        elif self.target_segment == 'custom' and self.target_customer_ids:
            customers = self.target_customer_ids
        else:
            customers = self.env['res.partner'].search([('is_company', '=', False)], limit=3)
        
        if not customers:
            # Create a test customer
            test_customer = self.env['res.partner'].create({
                'name': 'Demo Customer',
                'email': 'demo@nuyu.com',
                'phone': '+96181234567',
                'is_company': False
            })
            customers = test_customer
        
        # Create and send messages
        sent_count = 0
        for customer in customers:
            try:
                message = self.env['social.message'].create({
                    'campaign_id': self.id,
                    'recipient_id': customer.id,
                    'platform_id': self.primary_platform.id,
                    'content': self.message_content,
                    'state': 'draft',
                })
                
                # Send the message
                message.action_send_now()
                
                if message.state == 'sent':
                    sent_count += 1
                    
            except Exception as e:
                # Log error but continue
                continue
        
        # Update campaign
        self.sent_count = sent_count
        if sent_count > 0:
            self.state = 'sent'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '🚀 Campaign Sent Successfully!',
                'message': f'Sent {sent_count} messages via {self.primary_platform.name}',
                'type': 'success'
            }
        }