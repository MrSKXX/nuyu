odoo.define('pos_discount_enhancement.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PosDiscountProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            async _onClickDiscountInfo() {
                const order = this.env.pos.get_order();
                const orderline = order.get_selected_orderline();
                
                if (!orderline) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('No Product Selected'),
                        body: this.env._t('Please select a product line first to add discount information.'),
                    });
                    return;
                }

                if (orderline.get_discount() === 0) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('No Discount Applied'),
                        body: this.env._t('Please apply a discount to this product first.'),
                    });
                    return;
                }

                const { confirmed, payload } = await this.showPopup('DiscountInfoPopup', {
                    title: this.env._t('Discount Information'),
                    startingValue: orderline.get_discount_info(),
                });

                if (confirmed) {
                    orderline.set_discount_info(payload);
                    this.showPopup('ConfirmPopup', {
                        title: this.env._t('Success'),
                        body: this.env._t('Discount information has been saved.'),
                        confirmText: this.env._t('OK'),
                        cancelText: false,
                    });
                }
            }
        };

    Registries.Component.extend(ProductScreen, PosDiscountProductScreen);

    return ProductScreen;
});