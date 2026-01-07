/** @odoo-module **/
import { CustomerAddress } from "@portal/interactions/address";
import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";

patch(CustomerAddress.prototype, {
    setup() {
        super.setup();
        this.formMunicipalities = this.addressForm['res_municipality_id'];
    },

    _changeMunOption(selectElement, municipalities) {
        // empty existing options, only keep the placeholder.

        selectElement.innerHTML = "";
        if (municipalities.length) {
            municipalities.forEach((item) => {
                let option = new Option(item[1], item[0]);
                option.setAttribute("data-code", item[2]);
                selectElement.appendChild(option);
            });
            this._showInput("res_municipality_id");
        } else {
            this._hideInput("res_municipality_id");
        }
    },

    async onChangeState() {
        await this.waitFor(super.onChangeState(...arguments));

        const stateId = this.addressForm.state_id.value;

        let municipalities = [];
        let requiredMunicipality = false;

        if (stateId) {
            const data = await this.waitFor(rpc(`/l10n_cu/state_infos/${stateId}`, {
                address_type: this.addressType
            }));

            municipalities = data['municipalities'];
            requiredMunicipality = data['municipality_required'];
        }
        this._markRequired(this.formMunicipalities.name, requiredMunicipality);
        this._changeMunOption(this.formMunicipalities, municipalities);

    },

    async _onChangeCountry(init = false) {
        await this.waitFor(super._onChangeCountry(...arguments));


        if (this._getSelectedCountryCode() !== "CU") {
            this.formMunicipalities.innerHTML = "";
            this._hideInput("res_municipality_id");
        }
    }

});
