from odoo import models, fields, api

class SocialCampaign(models.Model):
    """
    Basic Social Campaign Model - Testing Version
    Start with minimal fields, add complexity later
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
    
    # Simple target segment (add custom option)
    target_segment = fields.Selection([
        ('all', 'All Customers'),
        ('vip', 'VIP Customers Only'),
        ('custom', 'Custom Selection')
    ], string='Target Segment', default='all')
    
    # Target customers for custom selection
    target_customer_ids = fields.Many2many('res.partner', string='Target Customers')
    
    # Link to platform (Many2one relationship)
    primary_platform = fields.Many2one('social.platform', string='Primary Platform')
    
    # Message content
    message_content = fields.Text(string='Message Content', required=True)
    
    # Simple scheduling
    send_immediately = fields.Boolean(string='Send Immediately', default=True)
    scheduled_date = fields.Datetime(string='Scheduled Date')
    
    # Basic statistics
    sent_count = fields.Integer(string='Messages Sent', default=0)
    
    # Relationship to messages
    message_ids = fields.One2many('social.message', 'campaign_id', string='Messages')
    
    def action_send_test(self):
        """Simple test send function"""
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
        
        # Get customers based on target segment
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
            # Create a test customer if none exist
            test_customer = self.env['res.partner'].create({
                'name': 'Demo Customer',
                'email': 'demo@nuyu.com',
                'is_company': False
            })
            customers = test_customer
        
        # Create messages for each customer
        for customer in customers:
            message = self.env['social.message'].create({
                'campaign_id': self.id,
                'recipient_id': customer.id,
                'platform_id': self.primary_platform.id,
                'content': self.message_content,
                'state': 'sent',
                'sent_date': fields.Datetime.now()
            })
        
        # Update campaign
        self.sent_count = len(customers)
        self.state = 'sent'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Campaign Sent!',
                'message': f'Campaign sent to {len(customers)} customers',
                'type': 'success'
            }
        }