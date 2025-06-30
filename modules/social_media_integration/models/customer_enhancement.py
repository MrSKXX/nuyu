from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    social_media_notes = fields.Text(string='Social Media Notes')
    preferred_contact_method = fields.Selection([
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('email', 'Email'),
        ('phone', 'Phone')
    ], string='Preferred Contact Method', default='whatsapp')
    
    birthday_campaign_sent = fields.Boolean(string='Birthday Campaign Sent This Year', default=False)
    last_birthday_campaign = fields.Date(string='Last Birthday Campaign')
    
    # Customer Segmentation - Auto-calculated based on sales
    total_spent = fields.Float(string='Total Spent', compute='_compute_total_spent', store=True)
    spending_tier = fields.Selection([
        ('vip', 'VIP ($2000+)'),
        ('medium', 'Medium ($1000-2000)'),
        ('low', 'Low (<$1000)')
    ], string='Customer Tier', compute='_compute_spending_tier', store=True)
    
    @api.depends('sale_order_ids.amount_total')
    def _compute_total_spent(self):
        for partner in self:
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            partner.total_spent = sum(orders.mapped('amount_total'))
    
    @api.depends('total_spent')
    def _compute_spending_tier(self):
        for partner in self:
            if partner.total_spent >= 2000:
                partner.spending_tier = 'vip'
            elif partner.total_spent >= 1000:
                partner.spending_tier = 'medium'
            else:
                partner.spending_tier = 'low'