from odoo import models, fields

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    discount_reason = fields.Selection([
        ('customer_loyalty', 'Customer Loyalty'),
        ('bulk_order', 'Bulk Order'),
        ('insurance_adjustment', 'Insurance Adjustment'),
        ('promotional', 'Promotional'),
        ('staff_discount', 'Staff Discount'),
        ('medical_necessity', 'Medical Necessity'),
        ('other', 'Other'),
    ], string='Discount Reason')
    
    discount_requested_by = fields.Char(string='Requested By')
    discount_approved_by = fields.Char(string='Approved By')