from odoo import models, fields, api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    discount_reason = fields.Selection([
        ('customer_loyalty', 'Customer Loyalty'),
        ('bulk_order', 'Bulk Order'),
        ('promotional', 'Promotional'),
        ('staff_discount', 'Staff Discount'),
        ('other', 'Other'),
    ], string='Discount Reason')
    
    discount_requested_by_id = fields.Many2one('res.partner', string='Requested By')
    discount_approved_by_id = fields.Many2one('res.partner', string='Approved By')
    
    discount_requested_by = fields.Char(string='Requested By Name')
    discount_approved_by = fields.Char(string='Approved By Name')
    
    discount_info_note = fields.Text(string='Discount Information', compute='_compute_discount_info', store=True)
    discount_timestamp = fields.Datetime(string='Discount Applied At', default=fields.Datetime.now)
    
    @api.depends('discount_reason', 'discount_requested_by', 'discount_approved_by')
    def _compute_discount_info(self):
        for line in self:
            if line.discount > 0 and line.discount_reason:
                reason_display = dict(line._fields['discount_reason'].selection).get(line.discount_reason, '')
                line.discount_info_note = f"{reason_display} - Req: {line.discount_requested_by or 'N/A'} - App: {line.discount_approved_by or 'N/A'}"
            else:
                line.discount_info_note = False

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def _process_order(self, order, draft, existing_order):
        """Enhanced order processing with discount info saving"""
        pos_order = super()._process_order(order, draft, existing_order)
        
        # Process discount information
        if order.get('lines'):
            for line_data in order['lines']:
                if len(line_data) >= 3 and isinstance(line_data[2], dict):
                    line_vals = line_data[2]
                    
                    # Check if this line has discount info from our JavaScript
                    if any(key.startswith('discount_') for key in line_vals.keys()):
                        # Find the corresponding order line
                        order_line = pos_order.lines.filtered(
                            lambda l: abs(l.qty - line_vals.get('qty', 0)) < 0.01 and 
                                     l.product_id.id == line_vals.get('product_id')
                        )[:1]
                        
                        if order_line:
                            # Prepare discount data
                            discount_data = {}
                            
                            if line_vals.get('discount_reason'):
                                discount_data['discount_reason'] = line_vals['discount_reason']
                            
                            if line_vals.get('discount_requested_by'):
                                discount_data['discount_requested_by'] = line_vals['discount_requested_by']
                            
                            if line_vals.get('discount_approved_by'):
                                discount_data['discount_approved_by'] = line_vals['discount_approved_by']
                            
                            # Try to find partner IDs if names were provided
                            if line_vals.get('discount_requested_by'):
                                partner = self.env['res.partner'].search([
                                    ('name', 'ilike', line_vals['discount_requested_by'])
                                ], limit=1)
                                if partner:
                                    discount_data['discount_requested_by_id'] = partner.id
                            
                            if line_vals.get('discount_approved_by'):
                                partner = self.env['res.partner'].search([
                                    ('name', 'ilike', line_vals['discount_approved_by'])
                                ], limit=1)
                                if partner:
                                    discount_data['discount_approved_by_id'] = partner.id
                            
                            # Save to database
                            if discount_data:
                                order_line.write(discount_data)
                                print(f"Saved discount info to database: {discount_data}")
        
        return pos_order