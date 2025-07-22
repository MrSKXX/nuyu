odoo.define('pos_custom_discount_tracker.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PosDiscountProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            mounted() {
                super.mounted();
                this._addDiscountButton();
            }

            _addDiscountButton() {
                setTimeout(() => {
                    const controlButtons = document.querySelector('.control-buttons');
                    
                    if (controlButtons && !controlButtons.querySelector('.discount-info-button')) {
                        const discountBtn = document.createElement('button');
                        discountBtn.className = 'btn btn-secondary btn-lg discount-info-button';
                        discountBtn.innerHTML = '<i class="fa fa-percent"></i> Discount Info';
                        discountBtn.style.marginLeft = '8px';
                        discountBtn.style.backgroundColor = '#f8f9fa';
                        discountBtn.style.borderColor = '#875a7b';
                        discountBtn.style.color = '#875a7b';
                        
                        discountBtn.onclick = () => this._onClickDiscountInfo();
                        
                        controlButtons.appendChild(discountBtn);
                        console.log('✅ Discount Info button added by module');
                    }
                }, 500);
            }

            _onClickDiscountInfo() {
                const order = this.env.pos.get_order();
                const orderline = order.get_selected_orderline();
                
                if (!orderline) {
                    alert('❌ Please select a product line first.');
                    return;
                }

                if (orderline.get_discount() === 0) {
                    alert('❌ Please apply a discount to this product first.');
                    return;
                }

                // Enhanced popup with better UX
                const reason = prompt(`💰 DISCOUNT INFORMATION
                
Select discount reason:
1. Customer Loyalty
2. Bulk Order  
3. Insurance Adjustment
4. Promotional
5. Staff Discount
6. Medical Necessity
7. Other

Enter number (1-7):`);
                
                if (!reason || reason < 1 || reason > 7) return;
                
                const requested = prompt('👤 Requested By (Employee Name):');
                if (!requested) return;
                
                const approved = prompt('✅ Approved By (Manager Name):');
                if (!approved) return;

                const reasons = ['', 'customer_loyalty', 'bulk_order', 'insurance_adjustment', 'promotional', 'staff_discount', 'medical_necessity', 'other'];
                const reasonLabels = ['', 'Customer Loyalty', 'Bulk Order', 'Insurance Adjustment', 'Promotional', 'Staff Discount', 'Medical Necessity', 'Other'];
                
                const reasonValue = reasons[reason];
                const reasonLabel = reasonLabels[reason];

                // Store the data in the orderline
                orderline.discount_reason = reasonValue;
                orderline.discount_requested_by = requested;
                orderline.discount_approved_by = approved;

                // Visual confirmation
                alert(`✅ DISCOUNT INFORMATION SAVED!

📋 Summary:
• Reason: ${reasonLabel}
• Requested by: ${requested}  
• Approved by: ${approved}
• Product: ${orderline.get_product().display_name}
• Discount: ${orderline.get_discount()}%

This information will be saved with the order.`);

                console.log('Discount info saved:', {
                    reason: reasonValue,
                    requested_by: requested,
                    approved_by: approved,
                    product: orderline.get_product().display_name,
                    discount: orderline.get_discount()
                });
            }
        };

    Registries.Component.extend(ProductScreen, PosDiscountProductScreen);

    return PosDiscountProductScreen;
});