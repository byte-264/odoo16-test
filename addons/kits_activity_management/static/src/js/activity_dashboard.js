/** @odoo-module */

import { registry } from "@web/core/registry";
import session from 'web.session';
import { useService } from "@web/core/utils/hooks";
import { Component,useState} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import {getCookie} from 'web.utils.cookies';

export class ActivityDashBoard extends Component {
    setup() {
        var self = this;
        this.reload_time = false;
        this._kitsTimeoutId = null;
        this.action = useService("action");
        this.state = useState({
            activity_counts: false,
            activity_data: false,
            models_data: false,
            users_data: false,
            activity_types_data: false,
            model_records_data: false,
            done_count: false,
            today_count: false,
            planned_count: false,
            overdue_count: false,
            isresult: false,
            user_role:false,
        });
        if (getCookie('cids')) {
            this.cids = this.parseCompanyIds(getCookie('cids'));
        }
        
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
        session.rpc('/kits-refresh-configuration', {})
        .then((result) => {
            self.reload_time = result;
            this.KitsGetActivitiesData();
        });

        session.rpc('/kits-get-user', {})
        .then((result) => {
            self.state.users_data = result;
        });

        session.rpc('/kits-get-user-role', {})
        .then((result) => {
            self.state.user_role = result;
        });

        window.onclick = function(event) {
            if (!event.target.closest('#KitsnavbarSupportedContent')) {
                if ($('.kits-navbar-collapse.show').length>0){
                    $('.kits-navbar-collapse.show').removeClass('show');
                }
            }
        }
    }

    parseCompanyIds(cids, separator = ",") {
        if (typeof cids === "string") {
            return cids.split(separator).map(Number);
        } else if (typeof cids === "number") {
            return [cids];
        }
        return [];
    }

    KitsopenActivity(id){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Activity'),
            target: 'current',
            res_id: parseInt(id),
            res_model: 'mail.activity',
            views: [[false, 'form']],
        });
    }

    CreateNewActivity(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Schedule Activity '),
            res_model: 'mail.activity',
            target: 'new',
            views: [[false, 'form']],
            context:{default_is_chatter:true}
        });
    }

    KitsGetFilters(){
        var side_filter = $('.kits-active')[0];
        var activity_state = $('#KitsStagesSelection').val();
        var user_id = $('#KitsUsersSelection').val();
        var model_name = $('#KitsModelsSelection').val();
        var record_id = $('#KitsrecordSelection').val();
        var activity_type_id = $('#KitsActivityTypesSelection').val();
        if (!side_filter){
            var side_filter = null;
        }
        else{
            var side_filter = side_filter.id;
        }
        if (!activity_state || activity_state == 'select_stages'){
            var activity_state = null;
        }
        if (!user_id || user_id == 'select_users'){
            var user_id = null;
        }
        if (!model_name || model_name == 'select_model'){
            var model_name = null;
        }
        if (!record_id || record_id == 'select_record'){
            var record_id = null;
        }
        if (!activity_type_id || activity_type_id == 'select_types'){
            var activity_type_id = null;
        }
        return {side_filter:side_filter,activity_state:activity_state,user_id:user_id,model_name:model_name,record_id:record_id,activity_type_id:activity_type_id,cids:this.cids}
    }

    KitsGetActivitiesData(){
        var self = this;
        if($('#KitsActivityDashboard').length>0 && this.reload_time){
            if (this.reload_time>0){
                //Clear Exsisting Schedul Actions
                if (this._kitsTimeoutId) {
                    clearTimeout(this._kitsTimeoutId);
                    this._kitsTimeoutId = null;
                }
                //Create New Schedule Actions
                let milliseconds = this.reload_time * 1000;
                this._kitsTimeoutId = setTimeout(() => {
                    this.KitsGetActivitiesData();
                }, milliseconds);
            }
        }
        var filters = this.KitsGetFilters();
        session.rpc('/get-data-for-activity-dashboard', filters)
        .then((result) => {
            self.state.isresult = true;
            self.state.activity_data = result.activity_data;
            self.state.done_count = result.done_count;
            self.state.today_count = result.today_count;
            self.state.planned_count = result.planned_count;
            self.state.overdue_count = result.overdue_count;
            self.state.models_data = result.all_models;
            self.state.activity_types_data = result.all_activity_type;
        })
    }

    FilterAllActivities(id,public_name){
        $('.kits-active').removeClass('kits-active');
        $("#"+id).addClass('kits-active');
        this.KitsGetActivitiesData();
        $('.kits-span').text(public_name);
        if ($(window).width() < 786) {
            $('.kits-side-panel').css('display', 'none');
        }
    }

    KitsOnSelectStage(){
        this.KitsGetActivitiesData();
    }

    KitsOnSelectUsers(){
        this.KitsGetActivitiesData();
    }

    KitsOnSelectModels(){
        var self = this;
        var model = $('#KitsModelsSelection').val();
        $('#KitsrecordSelection').val('select_record');
        this.KitsGetActivitiesData();
        if (model && model != "select_model"){
            session.rpc('/kits-get-model-records', {model:model})
            .then((result) => {
                self.state.model_records_data = result;
            })
        }
        else {
            this.state.model_records_data = false;

        }
    }
    KitsOnSelectrecords(){
        this.KitsGetActivitiesData();
    }
    KitsOnSelectActivityTypes(){
        this.KitsGetActivitiesData();
    }
    OpenMobileFIlter(){
        if ($(window).width() < 786) {
            if ($('.kits-side-panel').css('display') === 'block') {
                $('.kits-side-panel').css('display', 'none');
            } else {
                $('.kits-side-panel').css('display', 'block');
            }
        }
    }
}

ActivityDashBoard.template = "ActivityDashBoard";

registry.category("actions").add("activity_dashboard_tag", ActivityDashBoard,  { force: true });
