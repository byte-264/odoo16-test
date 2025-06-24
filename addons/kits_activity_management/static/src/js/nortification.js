/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Notification } from "@web/core/notifications/notification";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

patch(Notification.prototype,"KitsNotification",{
    setup(){
        this.state = useState({ message: false });

        try {
            let message = this.props.message;
            if(Array.isArray(message) && message[0]=='activity_reminder'){
                this.state.message = message;
            }
            
            } catch (error) {
                this.state.message = false;
            }
    }
});