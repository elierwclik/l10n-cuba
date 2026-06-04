/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list";
import { useService } from "@web/core/utils/hooks";
import { onMounted } from "@odoo/owl";

patch(PartnerList.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        onMounted(async () => {
            if (!this.pos.cnaes) {
                this.pos.cnaes = await this.orm.searchRead(
                    "res.cnae",
                    [],
                    ["id", "code", "name"],
                    { limit: 0 }
                );
            }
        });
    },

    getCnaes() {
        return this.pos.cnaes || [];
    },
});
