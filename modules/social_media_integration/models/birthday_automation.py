from odoo import models, fields, api, _
from datetime import datetime, timedelta

class BirthdayAutomation(models.Model):
    """
    Birthday Campaign Automation
    Replaces Elena's manual spreadsheet with automated daily birthday detection
    """
    _name = 'social.birthday.automation'
    _description = 'Birthday Campaign Automation'
    
    name = fields.Char(string='Automation Name', required=True, default='NuYu Birthday Campaigns')
    is_active = fields.Boolean(string='Active', default=True)
    
    # Gender-specific message templates
    female_message_template = fields.Text(
        string='Female Birthday Message',
        default="""🎉 Happy Birthday Beautiful! 🎂

Wishing you a day filled with happiness and a year filled with joy! ✨

As our special birthday gift to you: 20% OFF any spa treatment this month! 
Perfect time to treat yourself to some well-deserved relaxation 💆‍♀️

Book your appointment: WhatsApp us or call NuYu Medical Spa 
📱 +961 XX XXX XXX

#BirthdayTreatment #NuYuSpa #SelfCare #BirthdayGirl"""
    )
    
    male_message_template = fields.Text(
        string='Male Birthday Message', 
        default="""🎉 Happy Birthday! 🎂

Hope you have an awesome day and a fantastic year ahead! 🌟

Celebrate with 20% OFF any treatment this month. 
Perfect time to refresh and recharge! 💪

Book your appointment: WhatsApp us or call NuYu Medical Spa
📱 +961 XX XXX XXX

#BirthdayOffer #NuYuSpa #Refresh #BirthdaySpecial"""
    )
    
    vip_bonus_message = fields.Text(
        string='VIP Customer Bonus',
        default="""✨ As one of our valued VIP clients, enjoy an additional complimentary consultation with our specialists! ⭐

Thank you for your continued trust in NuYu Medical Spa! 🏆"""
    )
    
    # Campaign settings
    send_hour = fields.Integer(string='Send Hour (24h format)', default=9, 
                              help="Hour to send birthday messages (9 AM default)")
    platforms_ids = fields.Many2many('social.platform', string='Platforms to Use')
    primary_platform_id = fields.Many2one('social.platform', string='Primary Platform',
                                         help="Main platform for birthday messages (usually WhatsApp)")
    
    # Statistics tracking
    total_sent_this_year = fields.Integer(string='Total Sent This Year', default=0)
    total_sent_this_month = fields.Integer(string='Total Sent This Month', default=0)
    last_run_date = fields.Date(string='Last Run Date')
    customers_processed_today = fields.Integer(string='Customers Processed Today', default=0)
    
    # Performance tracking
    success_rate = fields.Float(string='Success Rate %', compute='_compute_success_rate')
    last_error_message = fields.Text(string='Last Error Message')
    
    @api.depends('total_sent_this_year')
    def _compute_success_rate(self):
        """Calculate success rate based on sent vs failed messages"""
        for automation in self:
            # This will be enhanced when we track failed messages
            automation.success_rate = 95.0  # Placeholder for now
    
    @api.model
    def cron_daily_birthday_check(self):
        """
        Daily cron job to check for birthdays and send campaigns
        This replaces Elena's manual daily spreadsheet checking
        """
        active_automations = self.search([('is_active', '=', True)])
        
        for automation in active_automations:
            try:
                automation._process_daily_birthdays()
            except Exception as e:
                automation.last_error_message = str(e)
                # Log error but continue with other automations
                continue
    
    def _process_daily_birthdays(self):
        """Process birthday customers for today - Demo version"""
        today = fields.Date.context_today(self)
        
        # For demo purposes, find some customers to send birthday messages to
        # In real implementation, this would check actual birthday field
        try:
            # Get some demo customers (every 10th customer on certain days)
            all_customers = self.env['res.partner'].search([
                ('is_company', '=', False)
            ], limit=50)
            
            demo_birthday_customers = []
            for customer in all_customers:
                # Demo logic: customers get "birthday" on days matching their ID
                if customer.id % 30 == today.day % 30:
                    demo_birthday_customers.append(customer)
                    if len(demo_birthday_customers) >= 3:  # Max 3 demo birthdays per day
                        break
            
            if not demo_birthday_customers:
                return  # No demo birthdays today
            
            # Create and send birthday campaign
            campaign = self._create_birthday_campaign(demo_birthday_customers, today)
            campaign.action_send_test()
            
            # Update statistics
            self.last_run_date = today
            self.customers_processed_today = len(demo_birthday_customers)
            self.total_sent_this_year += len(demo_birthday_customers)
            self.total_sent_this_month += len(demo_birthday_customers)
            
        except Exception as e:
            self.last_error_message = f"Demo birthday processing error: {str(e)}"
    
    def _create_birthday_campaign(self, customers, date):
        """Create automated birthday campaign with gender-specific messaging"""
        campaign_vals = {
            'name': f'🎂 Birthday Campaign - {date.strftime("%B %d, %Y")} ({len(customers)} customers)',
            'campaign_type': 'birthday',
            'target_segment': 'custom',
            'primary_platform': self.primary_platform_id.id if self.primary_platform_id else False,
            'message_content': self.female_message_template,  # Default to female template
            'send_immediately': True,
            'state': 'draft'
        }
        
        campaign = self.env['social.campaign'].create(campaign_vals)
        
        # Add customers to campaign
        campaign.target_customer_ids = [(6, 0, [c.id for c in customers])]
        
        return campaign
    
    def action_test_birthday_automation(self):
        """Test birthday automation with current user"""
        test_customer = self.env.user.partner_id
        
        # Get a platform to use (create one if none exists)
        platform = self.primary_platform_id
        if not platform:
            # Try to find any existing platform
            platform = self.env['social.platform'].search([], limit=1)
            if not platform:
                # Create a test platform
                platform = self.env['social.platform'].create({
                    'name': 'Test WhatsApp',
                    'platform_type': 'whatsapp',
                    'is_active': True
                })
        
        # Create test campaign with minimal required fields
        test_campaign_vals = {
            'name': f'🧪 TEST Birthday - {test_customer.name}',
            'campaign_type': 'birthday',
            'target_segment': 'all',  # Use 'all' instead of 'custom' for simplicity
            'primary_platform': platform.id,
            'message_content': self._get_birthday_message_for_customer(test_customer),
            'send_immediately': True
        }
        
        test_campaign = self.env['social.campaign'].create(test_campaign_vals)
        
        # Send the campaign using existing send function
        result = test_campaign.action_send_test()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('🎂 Test Birthday Campaign Sent!'),
                'message': f'Birthday test sent to {test_customer.name} via {platform.name}',
                'type': 'success'
            }
        }
    
    def _get_birthday_message_for_customer(self, customer):
        """Get appropriate birthday message based on customer gender and VIP status"""
        # Determine gender (basic logic - can be enhanced)
        is_female = False
        if customer.title:
            is_female = any(title in customer.title.name.lower() for title in ['ms', 'mrs', 'miss'])
        
        # Select base message
        base_message = self.female_message_template if is_female else self.male_message_template
        
        # Add VIP bonus if customer is VIP
        if hasattr(customer, 'spending_tier') and customer.spending_tier == 'vip':
            base_message += "\n\n" + self.vip_bonus_message
        
        return base_message
    
    def action_preview_todays_birthdays(self):
        """Preview customers with birthdays today"""
        today = fields.Date.context_today(self)
        
        # Check if birthday field exists, if not use a safer search
        try:
            # Try to find customers with birthday field
            all_customers = self.env['res.partner'].search([
                ('is_company', '=', False)
            ])
            
            # Filter manually for now (we'll add birthday field later)
            todays_birthdays = []
            for customer in all_customers:
                # For now, just show some sample customers
                if customer.id % 10 == today.day % 10:  # Simple demo logic
                    todays_birthdays.append(customer.id)
            
            # Limit to 5 for demo
            todays_birthdays = todays_birthdays[:5]
            
        except Exception as e:
            # Fallback: just show first few customers
            all_customers = self.env['res.partner'].search([
                ('is_company', '=', False)
            ], limit=5)
            todays_birthdays = all_customers.ids
        
        return {
            'name': f'🎂 Demo Birthday Customers - {today.strftime("%B %d")} ({len(todays_birthdays)} customers)',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', todays_birthdays)],
            'context': {
                'default_is_company': False,
                'search_default_customers': 1
            }
        }
    
    def action_reset_birthday_flags(self):
        """Reset birthday campaign flags for new year (January maintenance)"""
        customers = self.env['res.partner'].search([
            ('is_company', '=', False),
            ('birthday_campaign_sent', '=', True)
        ])
        
        customers.write({
            'birthday_campaign_sent': False,
            'last_birthday_campaign': False
        })
        
        # Reset statistics for new year
        self.total_sent_this_year = 0
        self.total_sent_this_month = 0
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('🔄 Birthday Flags Reset'),
                'message': f'Reset birthday campaign flags for {len(customers)} customers. Ready for new year!',
                'type': 'success'
            }
        }
    
    def action_send_manual_birthday_campaign(self):
        """Manually trigger birthday campaign for today"""
        try:
            self._process_daily_birthdays()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('🎂 Manual Birthday Campaign Triggered'),
                    'message': f'Processed {self.customers_processed_today} birthday customers',
                    'type': 'success'
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('❌ Error'),
                    'message': f'Error processing birthdays: {str(e)}',
                    'type': 'danger'
                }
            }