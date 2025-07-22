odoo.define('pos_discount_enhancement.models', function (require) {
    'use strict';

    const { Order, Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosDiscountOrderline = (Orderline) =>
        class extends Orderline {
            constructor(obj, options) {
                super(...arguments);
                this.discount_reason = this.discount_reason || '';
                this.discount_requested_by = this.discount_requested_by || '';
                this.discount_approved_by = this.discount_approved_by || '';
            }

            init_from_JSON(json) {
                super.init_from_JSON(json);
                this.discount_reason = json.discount_reason || '';
                this.discount_requested_by = json.discount_requested_by || '';
                this.discount_approved_by = json.discount_approved_by || '';
            }

            export_as_JSON() {
                const json = super.export_as_JSON();
                json.discount_reason = this.discount_reason;
                json.discount_requested_by = this.discount_requested_by;
                json.discount_approved_by = this.discount_approved_by;
                return json;
            }

            export_for_printing() {
                const json = super.export_for_printing();
                json.discount_reason = this.discount_reason;
                json.discount_requested_by = this.discount_requested_by;
                json.discount_approved_by = this.discount_approved_by;
                return json;
            }

            set_discount_info(discount_info) {
                this.discount_reason = discount_info.reason;
                this.discount_requested_by = discount_info.requested_by;
                this.discount_approved_by = discount_info.approved_by;
                this.trigger('change', this);
            }

            get_discount_info() {
                return {
                    reason: this.discount_reason,
                    requested_by: this.discount_requested_by,
                    approved_by: this.discount_approved_by,
                };
            }

            has_discount_info() {
                return this.discount_reason && this.discount_requested_by && this.discount_approved_by;
            }
        };

    Registries.Model.extend(Orderline, PosDiscountOrderline);

    return {
        PosDiscountOrderline,
    };
});