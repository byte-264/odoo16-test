/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ChatterContainer } from "@mail/components/chatter_container/chatter_container";
import session from 'web.session';
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(ChatterContainer.prototype, "KitsChatter",{
    setup() {
        var self = this;
        this._super(...arguments);
        this.state = useState({
            activityrecords: false,
        });
        this.action = useService("action");
        session.rpc('/fetch-activity-data', {
            threadmodel:this.props.threadModel,
           threadid:this.props.threadId,
        }).then((result) => {
            self.state.activityrecords = result;
        })
        const root = document.documentElement;
        session.rpc('/kits-get-colors', {})
        .then((result) => {
            root.style.setProperty('--kits-primary-color', result.primary_color || '#2c3e50');
            root.style.setProperty('--kits-hover-color', result.hover_color || '#34495e');
            root.style.setProperty('--kits-active-color', result.active_color || '#2980b9');
            root.style.setProperty('--kits-todays-color', result.todays_color || '#c5c7fb');
            root.style.setProperty('--kits-planned-color', result.planned_color || '#FFF4DE');
            root.style.setProperty('--kits-overdue-color', result.overdue_color || '#FFE2E5');
            root.style.setProperty('--kits-done-color', result.done_color || '#DCFCE7');
        })
    },

    async OpenActivity(activity_id){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Activity'),
            target: 'current',
            res_id: activity_id,
            res_model: 'mail.activity',
            views: [[false, 'form']],
        });
    },

});