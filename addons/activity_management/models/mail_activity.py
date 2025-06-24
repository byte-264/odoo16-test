# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from collections import defaultdict
from odoo import fields, models, api, modules, Command, _
from odoo.tools.misc import clean_context


def get_date(date_filter):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if date_filter == 'yesterday':
        end = today
        start = end - timedelta(1)
    elif date_filter == 'this_week':
        start = today - timedelta(days=datetime.today().weekday())
        end = start + timedelta(7)
    elif date_filter == 'this_month':
        start = today.replace(day=1)
        if start.month == 12:
            month = 1
        else:
            month = start.month + 1
        end = start.replace(month=month)
    elif date_filter == 'this_year':
        start = today.replace(day=1, month=1)
        end = start.replace(day=31, month=12)
    else:
        start = today.replace(day=1, month=1, year=today.year-1)
        end = start.replace(day=31, month=12)
    data = (start, end)
    return data


AVAILABLE_PRIORITIES = [
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Urgent')
]


class ActivityCheckLists(models.Model):
    _name = 'activity.checklist'
    _description = 'Activity Check List'

    name = fields.Char(string="Name", required=True)
    is_checked = fields.Boolean(string="Checked")
    activity_id = fields.Many2one('mail.activity')


class ActivityTags(models.Model):
    _name = 'activity.tag'
    _description = "Activity Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    complete_date = fields.Datetime(string="Completed On", readonly=True, store=True)
    state = fields.Selection(selection_add=[('done', "Done")], store=False)
    active = fields.Boolean(default=True)
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")
    description = fields.Html(string="Description", translate=True)
    checklist_progress = fields.Float(string="Progress", compute="_compute_progress_bar")
    activity_checklist_ids = fields.One2many('activity.checklist', 'activity_id', string="Checklist")
    tag_ids = fields.Many2many('activity.tag', string="Tags")
    color = fields.Integer(string="Color", compute='_get_color_state')

    @api.depends('state')
    def _get_color_state(self):
        for rec in self:
            if rec.state == 'overdue':
                rec.color = 1 # 1 danger 2 orange 10 green 4 info
            elif rec.state == 'done':
                rec.color = 10
            elif rec.state == 'today':
                rec.color = 2
            else:
                rec.color = 4

    @api.depends('activity_checklist_ids')
    def _compute_progress_bar(self):
        for rec in self:
            rec.checklist_progress = 0
            if rec.activity_checklist_ids:
                total_items = len(rec.activity_checklist_ids.ids)
                checked_item = len(rec.activity_checklist_ids.filtered(lambda item: item.is_checked is True))
                if total_items > 0 and checked_item > 0:
                    rec.checklist_progress = 100 * checked_item / total_items

    @api.depends('date_deadline')
    def _compute_state(self):
        for record in self.filtered(lambda activity: activity.date_deadline):
            if record.complete_date:
                record.state = 'done'
            else:
                tz = record.user_id.sudo().tz
                date_deadline = record.date_deadline
                record.state = self._compute_state_from_date(date_deadline, tz)


    def action_open_activity(self):
        ctx = dict(
            clean_context(self.env.context),
            default_previous_activity_type_id=self.activity_type_id.id,
            activity_previous_deadline=self.date_deadline,
            default_res_id=self.res_id,
            default_res_model=self.res_model,
        )
        return {
            'name': _('Schedule an Activity'),
            'context': ctx,
            'view_mode': 'form',
            'res_model': 'mail.activity',
            'views': [(False, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.chaining_type == 'trigger':
                vals = activity.with_context(activity_previous_deadline=activity.date_deadline)._prepare_next_activity_values()
                next_activities_values.append(vals)

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[Command.link(attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )

            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message

        next_activities = self.env['mail.activity'].create(next_activities_values)
        self.complete_date = fields.Datetime.now()
        self.active = False
        return messages, next_activities

    @api.model
    def get_activity_stats(self):
        manager = self.env.ref('activity_management.group_activity_manager')
        activity_user = self.env.ref('activity_management.group_activity_user')
        data = self.my_activity_data(user_id=self.env.user.id)
        data['is_admin'] = False
        if self.env.user.id in manager.users.ids:
            data['is_admin'] = True
            users = []
            for rec in activity_user.users:
                if rec.id != self.env.user.id:
                    users.append({'active': str(rec.id), 'name': rec.name})
            data['users'] = users
        return data

    @api.model
    def get_activity_stats_based_on_date(self, *kw):
        data = None
        if kw:
            manager = self.env.ref('activity_management.group_activity_manager')
            user_id = self.env.user.id
            if self.env.user.id in manager.users.ids:
                kw_length = len(kw) - 1
                if kw[kw_length] and kw[kw_length] == 'all_users':
                    user_id = False
                elif kw[kw_length] == 'my_activity':
                    pass
                else:
                    user_id = int(kw[kw_length])
            if kw[0] == 'all_time':
                data = self.my_activity_data(user_id=user_id)
            elif kw[0] == 'custom_range':
                start = datetime.strptime(kw[1], '%d/%m/%Y')
                end = datetime.strptime(kw[2], '%d/%m/%Y')
                date_filter = (start, end)
                data = self.my_activity_data(user_id=user_id, date_filter=date_filter)
            else:
                date_filter = get_date(kw[0])
                data = self.my_activity_data(user_id=user_id, date_filter=date_filter)
        return data

    @api.model
    def mark_done_event(self, *kw):
        mark_done = None
        if kw:
            activity = self.env['mail.activity'].sudo().search([('id', '=', kw[0]),
                                                                ('user_id', '=', self.env.user.id)], limit=1)
            if activity:
                activity.action_done()
                mark_done = True
        return mark_done

    def my_activity_data(self, user_id=None, date_filter=None):
        mail_activity = self.env['mail.activity'].sudo()
        activity_filter = [('active', 'in', (True, False))]
        if date_filter:
            activity_filter.append(('date_deadline', '>=', date_filter[0]))
            activity_filter.append(('date_deadline', '<=', date_filter[1]))
        if user_id:
            activity_filter.append(('user_id', '=', user_id))

        activities = mail_activity.search(activity_filter)

        today_activities = activities.filtered(lambda rec: rec.state == 'today')
        plan_activities = activities.filtered(lambda rec: rec.state == 'planned')
        overdue_activities = activities.filtered(lambda rec: rec.state == 'overdue')
        complete_activities = activities.filtered(lambda rec: rec.state == 'done')

        counts = {
            'all_count': len(activities.ids),
            'complete_count': len(complete_activities.ids),
            'plan_count': len(plan_activities.ids),
            'overdue_count': len(overdue_activities.ids),
        }

        data = {
            'graph': False,
            'stats': counts,
            'today': self.get_activity_object(today_activities),
            'all_activity': self.get_activity_object(activities),
            'plan': self.get_activity_object(plan_activities),
            'overdue': self.get_activity_object(overdue_activities),
            'complete': self.get_activity_object(complete_activities),
        }

        if not user_id:
            activity_user = self.env.ref('activity_management.group_activity_user')
            today_lst, plan_lst, overdue_lst, complete_lst, users = [], [], [], [], []
            for rec in activity_user.users:
                user_filter = activity_filter + [('user_id', '=', rec.id)]
                activities = mail_activity.search(user_filter)
                today_lst.append(len(activities.filtered(lambda rec: rec.state == 'today').ids))
                plan_lst.append(len(activities.filtered(lambda rec: rec.state == 'planned').ids))
                overdue_lst.append(len(activities.filtered(lambda rec: rec.state == 'overdue').ids))
                complete_lst.append(len(activities.filtered(lambda rec: rec.state == 'done').ids))
                users.append(rec.name)
            users_stats = {
                'today_list': today_lst,
                'plan_list': plan_lst,
                'overdue_list': overdue_lst,
                'complete_list': complete_lst,
                'users_list': users,
            }
            data['graph'] = True
            data['users_stats'] = users_stats
        return data

    def get_activity_object(self, activities):
        data = []
        for rec in activities:
            data.append({
                'title': rec.res_name,
                'activity_type': rec.activity_type_id.name,
                'user': rec.user_id.name,
                'date_deadline': rec.date_deadline,
                'activity_id': rec.id,
                'document_model': rec.res_model,
                'document_model_id': rec.res_model_id.id,
                'res_id': rec.res_id,
                'status': rec.state,
                'mark_done': bool(rec.complete_date),
            })
        return data

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        query = """SELECT m.id, count(*), act.res_model as model,
                            CASE
                                WHEN %(today)s::date - act.date_deadline::date = 0 Then 'today'
                                WHEN %(today)s::date - act.date_deadline::date > 0 Then 'overdue'
                                WHEN %(today)s::date - act.date_deadline::date < 0 Then 'planned'
                            END AS states
                        FROM mail_activity AS act
                        JOIN ir_model AS m ON act.res_model_id = m.id
                        WHERE user_id = %(user_id)s and active=True
                        GROUP BY m.id, states, act.res_model;
                        """
        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid,
        })
        activity_data = self.env.cr.dictfetchall()
        model_ids = [a['id'] for a in activity_data]
        model_names = {n[0]: n[1] for n in self.env['ir.model'].sudo().browse(model_ids).name_get()}

        user_activities = {}
        for activity in activity_data:
            if not user_activities.get(activity['model']):
                module = self.env[activity['model']]._original_module
                icon = module and modules.module.get_module_icon(module)
                user_activities[activity['model']] = {
                    'id': activity['id'],
                    'name': model_names[activity['id']],
                    'model': activity['model'],
                    'type': 'activity',
                    'icon': icon,
                    'total_count': 0, 'today_count': 0, 'overdue_count': 0, 'planned_count': 0,
                }
            user_activities[activity['model']]['%s_count' % activity['states']] += activity['count']
            if activity['states'] in ('today', 'overdue'):
                user_activities[activity['model']]['total_count'] += activity['count']

            user_activities[activity['model']]['actions'] = [{
                'icon': 'fa-clock-o',
                'name': 'Summary',
            }]
        return list(user_activities.values())
