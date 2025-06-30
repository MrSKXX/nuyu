from odoo import models, fields, api

class SocialPlatform(models.Model):
    """
    Basic Social Platform Model - Testing Version
    Start with minimal fields to ensure model creation works
    """
    _name = 'social.platform'
    _description = 'Social Media Platform'
    
    name = fields.Char(string='Platform Name', required=True)
    platform_type = fields.Selection([
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email')
    ], string='Platform Type', required=True)
    
    is_active = fields.Boolean(string='Active', default=False)
    
    # Simple fields first - we'll add complex ones later
    api_token = fields.Char(string='API Token')
    capabilities = fields.Text(string='Platform Capabilities')