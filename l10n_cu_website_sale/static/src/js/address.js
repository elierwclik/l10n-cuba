/** @odoo-module **/
import {rpc} from "@web/core/network/rpc";
import websiteSaleAddress from "@website_sale/js/address";


websiteSaleAddress.include({

    start: function () {
        this._super.apply(this, arguments);

        this.formState = this.addressForm.state_id;
        this.formMunicipalities = this.addressForm.res_municipality_id;

        this.country = this.addressForm.country_id;
    },

    _changeMunOption(selectElement, municipalities) {
        // empty existing options, only keep the placeholder.

        selectElement.innerHTML = '';
        if (municipalities.length) {
            municipalities.forEach((item) => {
                let option = new Option(item[1], item[0]);
                option.setAttribute('data-code', item[2]);
                selectElement.appendChild(option);
            });
            this._showInput('res_municipality_id');
        } else {
            this._hideInput('res_municipality_id');
        }
    },

    async _onChangeState(ev) {
        await this._super(...arguments);

        const stateId = this.formState.value;

        let municipalities = [];
        let requiredMunicipality = false;

        if (stateId) {
            const data = await rpc(`/shop/l10n_cu/state_infos/${stateId}`, {
                address_type: this.addressType
            });

            municipalities = data.municipalities;
            requiredMunicipality = data.municipality_required;
        }
        this._markRequired(this.formMunicipalities.name, requiredMunicipality);
        this._changeMunOption(this.formMunicipalities, municipalities);

    },

    async _changeCountry(init = false) {
        await this._super(...arguments);
        let selectedCountry = this.country.value ?
            this.country.selectedOptions[0].getAttribute('code') : '';

        if (selectedCountry !== 'CU') {
            this.formMunicipalities.innerHTML = '';
            this._hideInput('res_municipality_id');
        }
    },

});
