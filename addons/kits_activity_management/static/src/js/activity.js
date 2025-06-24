/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';
import rpc from 'web.rpc';

registerPatch({
    name: 'Activity',
    recordMethods: {
        async deleteServerRecord() {
            rpc.query({
                model: 'mail.activity',
                method: 'action_state_cancel',
                args: [[this.id]],
            });
        },
    },
});

registerPatch({
    name: 'Messaging',
    recordMethods: {
        async openActivityForm({ activity, defaultActivityTypeId, thread }) {
            const targetThread = activity && activity.thread || thread;
            const context = {
                default_res_id: targetThread.id,
                default_res_model: targetThread.model,
                default_is_chatter: true,
            };
            if (defaultActivityTypeId !== undefined) {
                context.default_activity_type_id = defaultActivityTypeId;
            }
            const action = {
                type: 'ir.actions.act_window',
                name: this.env._t("Schedule Activity"),
                res_model: 'mail.activity',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'new',
                context,
                res_id: activity ? activity.id : false,
            };
            return new Promise(resolve => {
                this.env.services.action.doAction(action, {
                    onClose: resolve,
                });
            });
        },
    },
});