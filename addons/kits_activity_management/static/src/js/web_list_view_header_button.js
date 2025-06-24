/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import session from 'web.session';
import { _t } from "@web/core/l10n/translation";

patch(ListController.prototype, "KitsListController",{
    async setup() {
        this._super(...arguments);
        this.kits_mass_activity_models = await session.rpc('/get-mass-activity-models', {})
    },

    async KitsCreateMassActivity() {
        const resModel = this.props.resModel;
        const resIds = await this.model.root.getResIds(true);
        this.actionService.doAction(
            {
                name: _t("Schedule Activity"),
                type: "ir.actions.act_window",
                res_model: "mass.activity.create.wizard",
                target: "new",
                views: [[false, "form"]],
                
                context: {default_model_name:resModel,default_rec_ids:resIds},
            },
        );
    }
});
