from odoo import models,fields,api
from ast import literal_eval

class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    def default_set_primary_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.primary_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.primary_color', '#2c3e50')
    def default_set_active_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.active_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.active_color', '#2980b9')
    def default_set_hover_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.hover_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.hover_color', '#34495e')
    def default_set_todays_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.todays_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.todays_color', '#c5c7fb')
    def default_set_planned_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.planned_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.planned_color', '#FFF4DE')
    def default_set_overdue_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.overdue_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.overdue_color', '#FFE2E5')
    def default_set_done_color(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.done_color'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.done_color', '#DCFCE7')
    def default_set_dashboard_refresh(self):
        if not self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.dashboard_refresh'):
            self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.dashboard_refresh', 5)

    kits_model_ids  = fields.Many2many('ir.model','kits_ir_model_and_res_config_rel','setting_id','model_id',domain=[('is_mail_activity','=',True),('is_mail_thread','=',True)],string="Models")
    dashboard_refresh = fields.Char(string="Dashboard refresh Time",config_parameter='kits_activity_management.dashboard_refresh',default=default_set_dashboard_refresh)
    primary_color = fields.Char(string="Primary Color",config_parameter='kits_activity_management.primary_color',default=default_set_primary_color)
    active_color = fields.Char(string="Active Color",config_parameter='kits_activity_management.active_color',default=default_set_active_color)
    hover_color = fields.Char(string="Hover Color",config_parameter='kits_activity_management.hover_color',default=default_set_hover_color)
    todays_color = fields.Char(string="Today's Color",config_parameter='kits_activity_management.todays_color',default=default_set_todays_color)
    planned_color = fields.Char(string="Planned Color",config_parameter='kits_activity_management.planned_color',default=default_set_planned_color)
    overdue_color = fields.Char(string="Overdue Color",config_parameter='kits_activity_management.overdue_color',default=default_set_overdue_color)
    done_color = fields.Char(string="Done Color",config_parameter='kits_activity_management.done_color',default=default_set_done_color)

    def set_values(self):
        res = super(res_config_settings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.model_ids', self.kits_model_ids.ids)
        return res
    
    @api.model
    def get_values(self):
        res = super(res_config_settings, self).get_values()
        models_params = self.env['ir.config_parameter'].sudo().get_param('kits_activity_management.model_ids')
        if models_params:
            res.update(kits_model_ids=[(6, 0, literal_eval(models_params))])
        return res
    
    def kits_reset_primary_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.primary_color', '#2c3e50')

    def kits_reset_active_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.active_color', '#2980b9')

    def kits_reset_hover_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.hover_color', '#34495e')

    def kits_reset_todays_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.todays_color', '#c5c7fb')
    
    def kits_reset_planned_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.planned_color', '#FFF4DE')
    
    def kits_reset_overdue_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.overdue_color', '#FFE2E5')
    
    def kits_reset_done_color(self):
        self.env['ir.config_parameter'].sudo().set_param('kits_activity_management.done_color', '#DCFCE7')