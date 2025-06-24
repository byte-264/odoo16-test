from odoo import models, fields, api, _
from odoo.tools.safe_eval import unsafe_eval, safe_eval, test_python_expr, datetime, dateutil, time
from odoo.exceptions import ValidationError, UserError
import logging
import datetime
import json
import decimal
import uuid
import re


class GoodEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, bytes):
            return "0x" + o.hex()
        if isinstance(o, models.Model):
            return {"__exec__": f"env['{o._name}'].browse({o.id})"}
        return super().default(o)


class GoodDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        self.vars = kwargs.pop('vars', {})
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        _logger.info(f"DECODER: {obj}")
        if '__exec__' in obj:
            result = unsafe_eval(obj['__exec__'], self.vars)
            return result
        return obj


_logger = logging.getLogger(__name__)

DEADLINE_REGEX = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2})\s*(?P<time>\d{2}:\d{2}:\d{2})?')
DEADLINE_NEXT_REGEX = re.compile(r'next\s+(?P<days>\d+)\s+days?|next\s+(?P<hours>\d+)\s+hours?')


class BPMProcessElement(models.Model):
    _name = 'bpm.process.element'

    name = fields.Char(string='Name')
    bpmn_id = fields.Char(string='BPMN ID', required=True, readonly=True)
    description = fields.Html(string='Description')
    process_id = fields.Many2one('bpm.process', string='Process', ondelete='cascade', required=True)
    source_ref = fields.Char(string='Source Ref', readonly=True)
    target_ref = fields.Char(string='Target Ref', readonly=True)
    condition = fields.Char(string='Condition')
    type = fields.Char(required=True, string='Type', readonly=True)
    code = fields.Text(string='Code')
    responsible = fields.Char(string='Responsible')
    groups = fields.Char(string='Groups')
    due_date = fields.Char(string='Due Date',
                           help="Use 'today' or 'tomorrow', 'next 3 days/hours' or date in ISO format '2024-01-01 12:00:00' for relative and fixed dates. Use python code for dynamic dates")
    create_notification = fields.Boolean(string='Create Notification')
    confirmation_type = fields.Selection([
        ('confirm', 'Confirm only'),
        ('approve', 'Approve and Cancel'),
    ], string='Confirmation Type', default='approve')
    default_flow = fields.Boolean(string='Default Flow')
    action_server_id = fields.Many2one(
        'ir.actions.server', 'Server Actions',
        domain="[('model_id', '=', process_id.model_id)]",
    )

    @api.depends('type', 'condition')
    def _compute_name(self):
        for rec in self:
            if not rec.name and rec.type.lower() == 'sequenceflow' and rec.condion:
                rec.name = rec.condition

    @api.constrains('type')
    def _check_type(self):
        for rec in self:
            if rec.type.lower() == 'usertask' and not rec.confirmation_type:
                raise ValidationError(_("Confirmation type is required for User Task"))

    @api.constrains('code')
    def _check_python_code(self):
        for action in self.sudo().filtered('code'):
            msg = test_python_expr(expr=action.code.strip(), mode="exec")
            if msg:
                raise ValidationError(msg)

    def _search_next(self):
        if self.type.lower() != 'sequenceflow':
            flow_elements = self.env['bpm.process.element'].search([('process_id', '=', self.process_id.id),
                                                                    ('source_ref', '=', self.bpmn_id)])
            next_tasks = []
            for flow_element in flow_elements:
                if flow_element.condition:
                    if not self._execute_script(flow_element.condition, mode="eval"):
                        continue
                next_element = self.env['bpm.process.element'].search([('process_id', '=', self.process_id.id),
                                                                       ('bpmn_id', '=', flow_element.target_ref)])

                next_tasks.append(next_element)
            return next_tasks

    def _execute_next(self):
        userTasks = self.env['project.task']
        for next_task in self._search_next():
            project_task = next_task._execute()
            userTasks += project_task
        return userTasks

    def _execute_script(self, code, mode="exec"):
        result = False
        instance_id = self.env.context.get('process_instance_id', False)
        if not instance_id:
            raise UserError(_('Process instance is required'))

        instance = self.env['bpm.process.instance'].browse(instance_id)
        if instance.context:
            context = json.loads(instance.context, cls=GoodDecoder, vars={'env': self.env})
            _logger.info(context)
        else:
            context = {}
        context.update(self.env.context)
        _logger.info(f"CONTEXT: {context}")
        if code:
            eval_context = {
                # 'datetime': safe_eval.datetime,
                # 'dateutil': safe_eval.dateutil,
                # 'time': safe_eval.time,
                'uid': self.env.uid,
                'user': self.env.user,
                'env': self.env,
                'logger': _logger,
                'result': False,
                'context': context,
                'ok': self.env.context.get('task_ok', False),
                'task': self.env.context.get('task', False),
            }
            result = safe_eval(code.strip(), eval_context,
                               mode=mode, nocopy=True
                               )

            instance.context = json.dumps(eval_context['context'], cls=GoodEncoder)
            if mode == "exec":
                result = eval_context['result']
        return result

    def _execute(self):
        self.ensure_one()
        instance_id = self.env.context.get('process_instance_id', False)
        if not instance_id:
            raise UserError(_('Process instance is required'))
        self.env['bpm.process.instance.element'].create({
            'instance_id': instance_id,
            'element_id': self.id,
        })

        userTasks = self.env['project.task']

        if self.type.lower() == 'usertask':
            if self.due_date:
                if self.due_date.lower() == 'today':
                    deadline = datetime.datetime.now()
                elif self.due_date.lower() == 'tomorrow':
                    deadline = datetime.datetime.now() + datetime.timedelta(days=1)
                elif DEADLINE_NEXT_REGEX.match(self.due_date):
                    match = DEADLINE_NEXT_REGEX.match(self.due_date)
                    if match.group('days'):
                        deadline = datetime.datetime.now() + datetime.timedelta(days=int(match.group('days')))
                    else:
                        deadline = datetime.datetime.now() + datetime.timedelta(hours=int(match.group('hours')))
                elif DEADLINE_REGEX.match(self.due_date):
                    match = DEADLINE_REGEX.match(self.due_date)
                    deadline = datetime.datetime.strptime(match.group('date'), "%Y-%m-%d")
                    if match.group('time'):
                        deadline = deadline.replace(hour=int(match.group('time').split(':')[0]),
                                                    minute=int(match.group('time').split(':')[1]),
                                                    second=int(match.group('time').split(':')[2]))
                else:
                    deadline = self._execute_script(self.due_date, mode="eval") if self.due_date else False
            else:
                deadline = False

            project_task = self.env['project.task'].create({
                'name': self.name,
                'description': self.description,
                'process_step_id': self.id,
                'user_ids': [(4, x, False) for x in
                             self._execute_script(self.responsible, mode="eval")] if self.responsible else [
                    (4, self.env.uid, False)],
                'project_id': False,
                'parent_id': False,
                'date_deadline': deadline,
                'process_instance_id': instance_id,

            })
            if self.create_notification:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': project_task.id,
                    'summary': project_task.summary,
                    'user_id': project_task.user_id.id,
                    'date_deadline': project_task.date_deadline,
                    'activity_type_id': self.env['mail.activity']._default_activity_type_for_model(
                        'project.task').id,
                })
            if self.code:
                self.with_context({
                    'task': project_task,
                    'process_instance_id': instance_id,
                })._execute_script(self.code)
            userTasks += project_task.filtered(lambda t: self.env.uid in [x.id for x in t.user_ids])

        if self.type.lower() in ('task', 'startevent', 'endevent',
                                 'intermediatecatchevent', 'exclusivegateway'):
            # Just pass the task
            userTasks += self._execute_next()
            pass
        if self.type.lower() == 'servicetask':
            # Execute the code
            userTasks += self._execute_next()
            pass
        if self.type.lower() == 'scripttask':
            self._execute_script(self.code)
            userTasks += self._execute_next()
            pass
        return userTasks
