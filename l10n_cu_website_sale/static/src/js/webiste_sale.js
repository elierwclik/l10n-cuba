/** @odoo-module **/
import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({

    _onChangeCountry: function (ev) {
        return this._super.apply(this, arguments).then(() => {
            if ($("#country_id").val()) {
                return this._onChangeState();
            }
        });
    },

    _onChangeState: function (ev) {
        return this._super.apply(this, arguments).then(() => {

            let state_id = ev ? ev.target.value : document.querySelector("select[name='state_id']").value;

            let mode = $("#country_id").attr('mode');
            if (!state_id) {
                this.$el.find("select[name='res_municipality_id']").val('').parent('div').hide();
                return;
            }

            return this.rpc("/shop/l10n_cu/state_infos/" + parseInt(state_id), {
                mode: mode
            }).then((data) => {
                return this._expandDataStates(data);
            })
        })
    },

    _expandDataStates(data) {
        // populate municipality and display
        var selectMunicipalities = $("select[name='res_municipality_id']");
        // dont reload state at first loading (done in qweb)
        if (selectMunicipalities.data('init') === 0 || selectMunicipalities.find('option').length === 1) {
            if (data.municipalities.length || data.municipality_required) {
                selectMunicipalities.html('');
                data.municipalities.forEach((x) => {
                    var opt = $('<option>').text(x[1])
                        .attr('value', x[0])
                        .attr('data-code', x[2]);
                    selectMunicipalities.append(opt);
                });
                selectMunicipalities.parent('div').show();
            } else {
                selectMunicipalities.val('').parent('div').hide();
            }
            selectMunicipalities.data('init', 0);
        } else {
            selectMunicipalities.data('init', 0);
        }

    }
});
