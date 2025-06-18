odoo.define('activity_management.ActivityDash', function (require) {
    'use strict';
    const AbstractAction = require('web.AbstractAction');
    const ajax = require('web.ajax');
    const core = require('web.core');
    const rpc = require('web.rpc');
    const session = require('web.session')
    const web_client = require('web.web_client');
    const _t = core._t;
    const QWeb = core.qweb;

    const ActionMenu = AbstractAction.extend({

        template: 'activityDashboard',

        events: {
            'change #activity_filter': 'onchange_activity_filter',
            'click .mark_done': 'activity_done',
            'click .view_activity': 'view_activity',
            'click .edit_activity': 'edit_activity',
            'click .activity-stats': 'view_activity_stats',
            'click #filter_activity': 'onclick_activity_filter',
            'change #activity_users': 'onchange_activity_user',
        },
        renderElement: function (ev) {
            const self = this;
            $.when(this._super())
                .then(function (ev) {
                    rpc.query({
                        model: "mail.activity",
                        method: "get_activity_stats",
                    }).then(function (data) {
                        $('input[name="filter_start_date"]').daterangepicker({
                            autoUpdateInput: false,
                            timePicker: false,
                            parentEl: '.scroll-fix',
                            singleDatePicker: true,
                            autoApply: true,
                            minDate: false,
                            showCustomRangeLabel: false,
                            locale: {
                                format: 'DD/MM/YYYY'
                            }
                        }, function (start, end, label) {
                        });
                        $('input[name="filter_start_date"]').on('apply.daterangepicker', function(ev, picker) {
                              $(this).val(picker.startDate.format('DD/MM/YYYY'));
                        });
                        $('input[name="filter_start_date"]').on('cancel.daterangepicker', function(ev, picker) {
                              $(this).val('');
                        });
                        $('input[name="filter_end_date"]').daterangepicker({
                            autoUpdateInput: false,
                            timePicker: false,
                            parentEl: '.scroll-fix',
                            singleDatePicker: true,
                            autoApply: true,
                            minDate: false,
                            showCustomRangeLabel: false,
                            locale: {
                                format: 'DD/MM/YYYY'
                            }
                        }, function (start, end, label) {
                        });
                        $('input[name="filter_end_date"]').on('apply.daterangepicker', function(ev, picker) {
                              $(this).val(picker.startDate.format('DD/MM/YYYY'));
                        });
                        $('input[name="filter_end_date"]').on('cancel.daterangepicker', function(ev, picker) {
                              $(this).val('');
                        });
                        if (data !== undefined) {
                             self.set_stats(data);
                             if(data['is_admin']){
                                 let user_options = ''
                                 for (let rec of data['users']){
                                     user_options += "<option value='"+rec['active']+"'>"+rec['name']+"</option>"
                                 }
                                 let select_ui = "<option value='all_users'>All Users</option>" +
                                     "<option value='my_activity' selected='selected'>My Activities</option>" + user_options
                                 $('#activity_users').empty().append(select_ui);
                             }
                        }
                    });
                });
        },
        apexGraph: function () {
            Apex.grid = {
                padding: {
                    right: 0,
                    left: 0,
                    top: 10,
                }
            }
            Apex.dataLabels = {
                enabled: false
            }
        },
        renderGraph: function(render_id, options){
            $(render_id).empty();
            const graphData = new ApexCharts(document.querySelector(render_id), options);
            graphData.render();
        },
        view_activity_stats: function (ev){
            ev.preventDefault();
            let activity_type = $(ev.currentTarget).data('type');
            let domain, context;
            domain = this.get_dates();
            let activity_user = $('#activity_users option:selected').val()
            if(activity_user){
                if(activity_user === 'my_activity'){
                    domain.push(['user_id', '=', session.uid])
                }else if(activity_user === 'all_users'){}
                else{
                    domain.push(['user_id', '=', parseInt(activity_user)])
                }
            }else{
                domain.push(['user_id', '=', session.uid])
            }
            domain.push(['active', 'in', [true, false]])
            if(activity_type === 'plan'){
                context = {'search_default_upcoming_activity': 1}
            } else if (activity_type === 'complete'){
                context = {'search_default_complete_activity': 1}
            }else if (activity_type === 'overdue'){
                context = {'search_default_overdue_activity': 1}
            }
            return this.do_action({
                name: _t("Activities"),
                type: 'ir.actions.act_window',
                domain: domain,
                res_model: 'mail.activity',
                view_mode: 'list',
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
                context: context,
            });
        },
        get_dates: function (){
            const searchFilter = $('#activity_filter option:selected').val();
            let filters = [];
            let start, end;
            let today = new Date();
            if(searchFilter === 'yesterday'){
                start = new Date(today);
                start.setDate(today.getDate() - 1);
                end = today
            }else if(searchFilter === 'this_week'){
                start = new Date(today.setDate(today.getDate() - today.getDay()));
                end = new Date(today.setDate(today.getDate() - today.getDay()+6));
            }else if(searchFilter === 'this_month'){
                start = new Date(today.getFullYear(), today.getMonth(), 1);
                end = new Date(today.getFullYear(), today.getMonth() + 1, 0);
            }else if(searchFilter === 'this_year'){
                start = new Date(today.getFullYear(), 1, 1);
                end = new Date(today.getFullYear(), 12, 31);
            }else if(searchFilter === 'pre_year'){
                start = new Date(today.getFullYear(), 1, 1);
                end = new Date(today.getFullYear(), 12, 31);
            }else if(searchFilter === 'custom_range'){
                let filter_start_date = $('#filter_start_date').val().split('/');
                let filter_end_date = $('#filter_end_date').val().split('/');
                start = new Date(filter_start_date[2], parseInt(filter_start_date[1])-1, filter_start_date[0]);
                end = new Date(filter_end_date[2], parseInt(filter_start_date[1])-1, filter_end_date[0]);
            }else {
                start = ''
                end = ''
            }
            if(start && end){
                filters.push(['date_deadline', '>=', start])
                filters.push(['date_deadline', '<=', end])
            }
            return filters
        },
        set_stats: function (result){
            $('#all_counts').empty().append(result['stats']['all_count']);
            $('#plan_counts').empty().append(result['stats']['plan_count']);
            $('#complete_counts').empty().append(result['stats']['complete_count']);
            $('#overdue_counts').empty().append(result['stats']['overdue_count']);

            this.get_activity('today-activities', result['today']);
            this.get_activity('all-activities', result['all_activity']);
            this.get_activity('plan-activities', result['plan']);
            this.get_activity('overdue-activities', result['overdue']);
            this.get_activity('complete-activities', result['complete']);
        },
        activity_done: function (ev){
            ev.preventDefault();
            rpc.query({
                model: "mail.activity",
                method: "mark_done_event",
                args: [$(ev.currentTarget).data('id')],
            }).then(function (data) {
                if (data) {
                    $(ev.currentTarget).addClass('d-none');
                }
            });
        },
        edit_activity: function (ev){
            this.get_action(ev, 'current');
        },
        view_activity: function (ev){
            this.get_action(ev, 'current');
        },
        get_action: function (ev, target){
            ev.preventDefault();
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: $(ev.currentTarget).data('model'),
                res_id: $(ev.currentTarget).data('res-id'),
                context: {
                    'active_id': $(ev.currentTarget).data('res-id')
                },
                views: [[false, 'form']],
                target: target
            });
        },
        get_activity: function (activity_id, result){
            let tag_id = "#"+activity_id
            const all_activities = $(tag_id).DataTable( {
                lengthChange: false,
                buttons: [ 'copy', 'excel', 'pdf', 'colvis' ],
                 "columns": [
                     {"width": "25%" },
                     {"width": "15%" },
                     {"width": "15%" },
                     {"width": "15%" },
                     {"width": "15%" },
                     {"width": "15%" },
                 ],
                "bDestroy": true
            });
            all_activities.clear().draw();
            for (let res of result) {
                let action_col = this.get_activity_details(res)
                all_activities.row.add(action_col[0]).draw().node();
            }
            all_activities.buttons().container().appendTo( tag_id+'_wrapper .col-md-6:eq(0)' );
        },
        get_activity_details : function(result){
            let status = ''
            if(result['status'] === 'done'){
                status += "<span class='badge badge-light-success fs-7 fw-bolder'>Completed</span>"
            } else if (result['status'] === 'planned'){
                status += "<span class='badge badge-light-info fs-7 fw-bolder'>Planned</span>"
            } else if (result['status'] === 'overdue'){
                status += "<span class='badge badge-light-danger fs-7 fw-bolder'>Overdue</span>"
            } else {
                status += "<span class='badge badge-light-warning fs-7 fw-bolder'>Today</span>"
            }

            let mark_done_activity = ''
            if(result['mark_done'] === false){
                mark_done_activity += "<a class='btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1 mark_done' title='Mark as done' data-id='"+result['activity_id']+"'>" +
                "        <span class='svg-icon svg-icon-3'>" +
                "           <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none'>" +
                "            <path opacity='0.5' d='M12.8956 13.4982L10.7949 11.2651C10.2697 10.7068 9.38251 10.7068 8.85731 11.2651C8.37559 11.7772 8.37559 12.5757 8.85731 13.0878L12.7499 17.2257C13.1448 17.6455 13.8118 17.6455 14.2066 17.2257L21.1427 9.85252C21.6244 9.34044 21.6244 8.54191 21.1427 8.02984C20.6175 7.47154 19.7303 7.47154 19.2051 8.02984L14.061 13.4982C13.7451 13.834 13.2115 13.834 12.8956 13.4982Z' fill='black'/>" +
                "            <path d='M7.89557 13.4982L5.79487 11.2651C5.26967 10.7068 4.38251 10.7068 3.85731 11.2651C3.37559 11.7772 3.37559 12.5757 3.85731 13.0878L7.74989 17.2257C8.14476 17.6455 8.81176 17.6455 9.20663 17.2257L16.1427 9.85252C16.6244 9.34044 16.6244 8.54191 16.1427 8.02984C15.6175 7.47154 14.7303 7.47154 14.2051 8.02984L9.06096 13.4982C8.74506 13.834 8.21146 13.834 7.89557 13.4982Z' fill='black'/>" +
                "           </svg>" +
                "        </span>" +
                "    </a>"
            }
            let activity = $("<tr>" +
                "<td class='fw-bolder'>"+result['title']+"</td>" +
                "<td><span class='badge badge-light-primary fs-7 fw-bolder'>"+result['activity_type']+"</span></td>" +
                "<td>"+result['user']+"</td>" +
                "<td>"+result['date_deadline']+"</td>" +
                "<td class='text-center'>"+status+"</td>" +
                "<td>" + mark_done_activity +
                "    <a class='btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1 edit_activity' title='Edit Activity' data-model='mail.activity' data-res-id='"+result['activity_id']+"'>" +
                "        <span class='svg-icon svg-icon-3'>" +
                "            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none'>" +
                "                <path opacity='0.3' d='M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z' fill='black'/>" +
                "                <path d='M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z' fill='black'/>" +
                "            </svg>" +
                "        </span>" +
                "    </a>" +
                "    <a class='btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1 view_activity' title='View origin of activity' data-model='"+result['document_model']+"' data-res-id='"+result['res_id']+"'>" +
                "        <span class='svg-icon svg-icon-3'>" +
                "            <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none'>" +
                "                <rect opacity='0.3' width='12' height='2' rx='1' transform='matrix(-1 0 0 1 15.5 11)' fill='black'/>" +
                "                <path d='M13.6313 11.6927L11.8756 10.2297C11.4054 9.83785 11.3732 9.12683 11.806 8.69401C12.1957 8.3043 12.8216 8.28591 13.2336 8.65206L16.1592 11.2526C16.6067 11.6504 16.6067 12.3496 16.1592 12.7474L13.2336 15.3479C12.8216 15.7141 12.1957 15.6957 11.806 15.306C11.3732 14.8732 11.4054 14.1621 11.8756 13.7703L13.6313 12.3073C13.8232 12.1474 13.8232 11.8526 13.6313 11.6927Z' fill='black'/>" +
                "                <path d='M8 5V6C8 6.55228 8.44772 7 9 7C9.55228 7 10 6.55228 10 6C10 5.44772 10.4477 5 11 5H18C18.5523 5 19 5.44772 19 6V18C19 18.5523 18.5523 19 18 19H11C10.4477 19 10 18.5523 10 18C10 17.4477 9.55228 17 9 17C8.44772 17 8 17.4477 8 18V19C8 20.1046 8.89543 21 10 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3H10C8.89543 3 8 3.89543 8 5Z' fill='#C4C4C4'/>" +
                "            </svg>" +
                "        </span>" +
                "    </a>" +
                "</td>" +
                "</tr>");
            return activity
        },
        get_activity_by_change: function (ev){
            const searchFilter = $('#activity_filter option:selected').val();
            const active_user = $('#activity_users option:selected').val();
            const self = this;
            if(searchFilter === 'custom_range'){
                $('.custom_search').removeClass('d-none');
            }else{
                $('.custom_search').addClass('d-none');
                rpc.query({
                    model: "mail.activity",
                    method: "get_activity_stats_based_on_date",
                    args: [searchFilter, active_user],
                }).then(function (data) {
                    if (data !== undefined) {
                         self.set_stats(data);
                         if(data['graph']){
                             self.getUserdata(data['users_stats']);
                            $('.all_users_activities').removeClass('d-none');
                         }else{
                             $('.all_users_activities').addClass('d-none');
                         }
                    }
                });
            }
        },
        onchange_activity_filter: function (ev) {
            this.get_activity_by_change(ev);
        },
        onchange_activity_user: function (ev) {
            this.get_activity_by_change(ev);
        },
        onclick_activity_filter: function (ev) {
            ev.preventDefault();
            const searchFilter = $('#activity_filter option:selected').val();
            const self = this;
            if(searchFilter === 'custom_range'){
                rpc.query({
                    model: "mail.activity",
                    method: "get_activity_stats_based_on_date",
                    args: ['custom_range', $('#filter_start_date').val(), $('#filter_end_date').val(), $('#activity_users option:selected').val()],
                }).then(function (data) {
                    if (data !== undefined) {
                         self.set_stats(data);
                         if(data['graph']){
                             self.getUserdata(data['users_stats']);
                            $('.all_users_activities').removeClass('d-none');
                         }else{
                             $('.all_users_activities').addClass('d-none');
                         }
                    }
                });
            }
        },
        getUserdata: function(data){
            const options = {
                series: [{
                  name: 'Planned Activities',
                  data: data['plan_list']
                },{
                  name: 'Completed Activities',
                  data: data['complete_list']
                },{
                  name: 'Today Activities',
                  data: data['today_list']
                },  {
                  name: 'Overdue Activities',
                  data: data['overdue_list']
                }],
                chart: {
                    type: 'bar',
                    height: 350,
                    stacked: true,
                    toolbar: {
                        show: true
                    },
                    zoom: {
                        enabled: true
                    }
                },
                plotOptions: {
                  bar: {
                    horizontal: false,
                    borderRadius: 10
                  },
                },
                responsive: [{
                  breakpoint: 480,
                  options: {
                    legend: {
                      position: 'bottom',
                      offsetX: -10,
                      offsetY: 0
                    }
                  }
                }],
                colors: ['#7FDBDA', '#ADE498', '#EDE682',  '#FEBF63'],
                xaxis: {
                  categories: data['users_list'],
                },
                fill: {
                  opacity: 1
                },
                legend: {
                  position: 'right',
                  offsetX: 0,
                  offsetY: 50
                },
            };
            this.renderGraph("#all_user_activities", options);
        },
        willStart: function () {
            const self = this;
            return this._super()
            .then(function() {});
        },
    });
    core.action_registry.add('activity_management', ActionMenu);

});
