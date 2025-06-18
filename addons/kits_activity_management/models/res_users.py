from odoo import _,models,api,modules
from collections import defaultdict

class res_users(models.Model):
    _inherit = 'res.users'

    # Replace This Method Is For In Header Activity
    @api.model
    def systray_get_activities(self):
        search_limit = int(self.env['ir.config_parameter'].sudo().get_param('mail.activity.systray.limit', 1000))
        activities = self.env["mail.activity"].search(
            [("user_id", "=", self.env.uid)], order='id desc', limit=search_limit)
        activities_by_record_by_model_name = defaultdict(lambda: defaultdict(lambda: self.env["mail.activity"]))
        for activity in activities:
            record = self.env[activity.res_model].browse(activity.res_id)
            activities_by_record_by_model_name[activity.res_model][record] += activity
        activities_by_model_name = defaultdict(lambda: self.env["mail.activity"])
        for model_name, activities_by_record in activities_by_record_by_model_name.items():
            if self.env[model_name].check_access_rights('read', raise_exception=False):
                res_ids = [r.id for r in activities_by_record]
                allowed_records = self.env[model_name].browse(res_ids)._filter_access_rules('read')
            else:
                allowed_records = self.env[model_name]
            for record, activities in activities_by_record.items():
                if record not in allowed_records:
                    activities_by_model_name['mail.activity'] += activities
                else:
                    activities_by_model_name[model_name] += activities
        model_ids = [self.env["ir.model"]._get_id(name) for name in activities_by_model_name]
        user_activities = {}
        for model_name, activities in activities_by_model_name.items():
            Model = self.env[model_name]
            module = Model._original_module
            icon = module and modules.module.get_module_icon(module)
            model = self.env["ir.model"]._get(model_name).with_prefetch(model_ids)
            user_activities[model_name] = {
                "id": model.id,
                "name": model.name,
                "model": model_name,
                "type": "activity",
                "icon": icon,
                "total_count": 0,
                "today_count": 0,
                "overdue_count": 0,
                "planned_count": 0,
                #start
                "done_count":0,
                "cancel_count":0,
                #end
                "view_type": getattr(Model, '_systray_view', 'list'),
            }
            if model_name == 'mail.activity':
                user_activities[model_name]['activity_ids'] = activities.ids
            for activity in activities:
                user_activities[model_name]["%s_count" % activity.state] += 1
                if activity.state in ("today", "overdue"):
                    user_activities[model_name]["total_count"] += 1
        if "mail.activity" in user_activities:
            user_activities["mail.activity"]["name"] = _("Other activities")
        return list(user_activities.values())
