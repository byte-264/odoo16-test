from odoo import http
from odoo.http import request
from ast import literal_eval
import json

class activity_fetch_controller(http.Controller):

    #For Chatter Data fetch
    @http.route('/fetch-activity-data' ,type='json', auth='user', methods=['POST'])
    def fetch_activity_data(self, **kw):
        result=[]
        try:
            data = request.dispatcher.jsonrequest
            threadmodel = data['params']['threadmodel']
            threadid = data['params']['threadid']
            result = request.env['mail.activity'].search_read(domain=[('res_model','=',threadmodel),('res_id','=',threadid)],
                                                                fields=['id', 'activity_type_id', 'user_id','summary','date_deadline','state'],
                                                                order='date_deadline DESC')
            return result 
        except:
            return result
    
    #In Listview Get Selected Models For Mass Activity Creation
    @http.route('/get-mass-activity-models' ,type='json', auth='user', methods=['POST'])
    def get_mass_activity_models(self, **kw):
        models_list = []
        try:
            models_params = request.env['ir.config_parameter'].sudo().get_param('kits_activity_management.model_ids')
            if models_params:
                for model in literal_eval(models_params):
                    model_id = request.env['ir.model'].sudo().search([('id','=',model)])
                    models_list.append(model_id.model)
            return models_list
        except:
            return models_list
    
    # For Dashboard
    @http.route('/get-data-for-activity-dashboard' ,type='json', auth='user', methods=['POST'])
    def get_data_for_activity_dashborard(self, **kw):
        try:
            data = request.dispatcher.jsonrequest
            side_filter = data['params']['side_filter']
            activity_state = data['params']['activity_state']
            record_id = data['params']['record_id']
            activity_type_id = data['params']['activity_type_id']
            user_id = data['params']['user_id']
            model_name = data['params']['model_name']
            cids=data['params']['cids']
            dict={"side_filter":None,"activity_state":None,"record_id":None,"activity_type_id":None,"login_user_id":None,"user_id":None,"model_name":None,"user_role":None,"cids":None}
            dict['login_user_id']=request.env.uid
            if request.env.user.has_group("kits_activity_management.kits_group_activity_admin"):
                dict['user_role']='admin'
            elif request.env.user.has_group("kits_activity_management.kits_group_activity_manager"):
                dict['user_role']='manager'
            elif request.env.user.has_group("kits_activity_management.kits_group_activity_user"):
                dict['user_role']='user'
            if side_filter:
                dict['side_filter']=side_filter
            if activity_state:
                dict['activity_state']=activity_state
            if record_id:
                dict['record_id']=record_id
            if activity_type_id:
                dict['activity_type_id']=activity_type_id
            if user_id:
                dict['user_id']=user_id
            if model_name:
                dict['model_name']=model_name
            if cids:
                dict['cids']=cids
            json_dict=json.dumps(dict)
            request.env.cr.execute("CALL kits_get_activity_data(%s)", (json_dict,))
            result = request.env.cr.fetchall()
            return result[0][0]
        except:
            return "can't access Api"
    
    @http.route('/kits-get-model-records' ,type='json', auth='user', methods=['POST'])
    def kits_get_model_records(self, **kw):
        records = []
        try:
            data = request.dispatcher.jsonrequest
            model = data['params']['model']
            records = request.env[model].sudo().search_read([],["name"])
            return records
        except:
            return records
    
    @http.route('/kits-refresh-configuration' ,type='json', auth='user', methods=['POST'])
    def kits_refresh_configuration(self, **kw):
        try:
            dashboard_reload_time = request.env['ir.config_parameter'].sudo().get_param('kits_activity_management.dashboard_refresh')
            if dashboard_reload_time:
                return int(dashboard_reload_time)
            else:
                return False
        except:
            return False
    
    @http.route('/kits-get-user-role' ,type='json', auth='user', methods=['POST'])
    def kits_get_user_role(self, **kw):
        result = False
        try:
            if request.env.user.has_group("kits_activity_management.kits_group_activity_admin"):
                result='admin'
            elif request.env.user.has_group("kits_activity_management.kits_group_activity_manager"):
                result='manager'
            elif request.env.user.has_group("kits_activity_management.kits_group_activity_user"):
                result='user'
            return result
        except:
            return result
    
    @http.route('/kits-get-user' ,type='json', auth='user', methods=['POST'])
    def kits_get_user(self, **kw):
        result = False
        try:
            user_role =  self.kits_get_user_role()
            if user_role == 'admin' or user_role == 'manager':
                result = request.env['res.users'].search_read(domain=[],fields=['name'])
            return result
        except:
            return result
    
    @http.route('/kits-get-colors' ,type='json', auth='user', methods=['POST'])
    def kits_get_colors(self, **kw):
        try:
            config_parameter_obj = request.env['ir.config_parameter']
            primary_color = config_parameter_obj.sudo().get_param('kits_activity_management.primary_color')
            active_color = config_parameter_obj.sudo().get_param('kits_activity_management.active_color')
            hover_color = config_parameter_obj.sudo().get_param('kits_activity_management.hover_color')
            todays_color = config_parameter_obj.sudo().get_param('kits_activity_management.todays_color')
            planned_color = config_parameter_obj.sudo().get_param('kits_activity_management.planned_color')
            overdue_color = config_parameter_obj.sudo().get_param('kits_activity_management.overdue_color')
            done_color = config_parameter_obj.sudo().get_param('kits_activity_management.done_color')
            colors = {'primary_color':primary_color,'active_color':active_color,'hover_color':hover_color,
                      'todays_color':todays_color,'planned_color':planned_color,'overdue_color':overdue_color,
                      'done_color':done_color}
            return colors
        except:
            return "can't access Api"