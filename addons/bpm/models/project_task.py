from odoo import api, models, fields, _, _lt, Command
from odoo.tools import html2plaintext


class Task(models.Model):
    _inherit = 'project.task'
    state = fields.Selection([
        ('01_in_progress', 'In Progress'),
        ('02_changes_requested', 'Changes Requested'),
        ('03_approved', 'Approved'),
        ('1_done', 'Done'),
        ('1_canceled', 'Canceled'),
        ('04_waiting_normal', 'Waiting'),
    ], string='State', copy=False, default='01_in_progress', required=True,
        readonly=False, store=True, index=True, recursive=True, tracking=True)
    personal_stage_id = fields.Many2one('project.task.stage.personal', string='Personal Stage State',
                                        compute_sudo=False, store=True,
                                        compute='_compute_personal_stage_id', help="The current user's personal stage.")

    process_step_id = fields.Many2one('bpm.process.element', string='Process Step', readonly=True)
    process_id = fields.Many2one('bpm.process', string='Process', related='process_instance_id.process_id', store=True)
    process_instance_id = fields.Many2one('bpm.process.instance', string='Process Instance', readonly=True)


    def action_convert_to_task(self):
        self.ensure_one()
        self.company_id = self.project_id.company_id
        return {
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
        }

    def action_complete_task(self):
        if self.process_step_id:
            userTasks = self.process_step_id.with_context({
                'process_instance_id': self.process_instance_id.id,
                'task_ok': True,
            })._execute_next()
        self.write({'state': '1_done', 'process_step_id': False})
        return userTasks.user_task_result()

    def action_reject_task(self):
        if self.process_step_id:
            userTasks = self.process_step_id.with_context({
                'process_instance_id': self.process_instance_id.id,
                'task_ok': False,
            })._execute_next()
        self.write({'state': '1_canceled', 'process_step_id': False})
        return userTasks.user_task_result()

    def user_task_result(self):
        if len(self) == 1:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'name': self.name,
                'views': [(False, 'form'), (False, 'kanban'), (False, 'tree')],
                'res_id': self.id,
                'domain': [('user_ids', 'in', [self.env.uid]), ('project_id', '=', False), ('parent_id', '=', False),
                           ('state', 'in',
                            ['01_in_progress', '02_changes_requested', '03_pproved', '04_waiting_normal'])],
                'context': {'search_default_open_tasks': 1},
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'name': 'Tasks',
                'views': [(False, 'kanban'), (False, 'tree'), (False, 'form')],
                'domain': [('user_ids', 'in', [self.env.uid]), ('project_id', '=', False), ('parent_id', '=', False),
                           ('state', 'in',
                            ['01_in_progress', '02_changes_requested', '03_pproved', '04_waiting_normal'])],
                'context': {'search_default_open_tasks': 1},
                'target': 'current',
            }
