from odoo import models, fields, api

class SocialMessage(models.Model):
    """
    Basic Social Message Model - Testing Version
    Individual messages sent through campaigns
    """
    _name = 'social.message'
    _description = 'Social Media Message'
    
    name = fields.Char(string='Message Reference', compute='_compute_name', store=True)
    
    # Relationships
    campaign_id = fields.Many2one('social.campaign', string='Campaign')
    recipient_id = fields.Many2one('res.partner', string='Recipient', required=True)
    platform_id = fields.Many2one('social.platform', string='Platform', required=True)
    
    # Content
    content = fields.Text(string='Message Content', required=True)
    
    # Status and dates
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ], string='Status', default='draft')
    
    sent_date = fields.Datetime(string='Sent Date')
    
    @api.depends('recipient_id', 'platform_id')
    def _compute_name(self):
        for message in self:
            if message.recipient_id and message.platform_id:
                message.name = f"{message.platform_id.platform_type.title()} to {message.recipient_id.name}"
            else:
                message.name = f"Message {message.id}"