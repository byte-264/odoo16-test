from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree
import re

BPMN_ELEMENTS_TYPES = [
    'sequenceflow',
    'startevent',
    'endevent',
    'task',
    'usertask',
    'servicetask',
    'scripttask',
    'parallelgateway',
    'exclusivegateway',
    'inclusivegateway',
]


class BPMProcess(models.Model):
    _name = 'bpm.process'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    res_model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related='res_model_id.model', string='Model Name', store=True)
    model_description = fields.Char(related='res_model_id.name', string='Model Description', store=True)
    element_ids = fields.One2many('bpm.process.element', 'process_id', string='Elements')
    xml = fields.Text(string='XML')
    screenshot = fields.Binary(string='Screenshot')
    user_ids = fields.Many2many('res.users', string='Users')
    group_ids = fields.Many2many('res.groups', string='Groups',
                                 default=lambda self: [(4, self.env.ref('base.group_user').id, False)])

    instance_ids = fields.One2many('bpm.process.instance', 'process_id', string='Instances')
    active = fields.Boolean(string='Active', default=True)
    enabled = fields.Boolean(string='Enabled', default=True)
    active_instance_count = fields.Integer(string='Active Instances', compute='_compute_active_instance_count')


    def _compute_active_instance_count(self):
        for rec in self:
            rec.active_instance_count = len(rec.instance_ids.filtered(lambda x: x.state == 'in_progress'))

    def action_start_process(self):
        self.ensure_one()
        process_instance = self.env['bpm.process.instance'].create({
                'process_id': self.id,
                'state': 'in_progress',
                'res_model_id': self.res_model_id.id,
                'model_name': self.model_name,
                'res_id': self.env.context.get('res_id', False),
            })
        start = self.env['bpm.process.element'].search(
            [('process_id', '=', self.id), ('type', '=', 'startEvent')], limit=1)

        if not start:
            raise UserError(_('No start event found in the process'))

        userTasks = start.with_context({'process_instance_id': process_instance.id})._execute()
        return userTasks.user_task_result()

    def write(self, vals):
        if 'xml' in vals:
            xml = vals['xml']
            try:
                name_template = r'\{.*\}(\w+)'
                root = etree.fromstring(xml.encode('utf-8'))
                element_ids = []
                bpmn_elements = [x.bpmn_id for x in self.element_ids]
                new_bpmn_elements = []
                for element in root.iter():
                    match = re.match(name_template, element.tag)
                    if match:
                        tag = match.group(1)
                        if tag.lower() in BPMN_ELEMENTS_TYPES:
                            new_bpmn_elements.append(element.attrib.get('id'))
                            if element.attrib.get('id') not in bpmn_elements:
                                data = {
                                    'bpmn_id': element.attrib.get('id'),
                                    'name': element.attrib.get('name'),
                                    'type': tag,
                                    'process_id': self.id,
                                }
                                if tag.lower() == 'sequenceflow':
                                    data['source_ref'] = element.attrib.get('sourceRef')
                                    data['target_ref'] = element.attrib.get('targetRef')

                                element_ids.append((0, 0, data))
                            if element.attrib.get('id') in bpmn_elements:
                                data = {
                                    'bpmn_id': element.attrib.get('id'),
                                    'type': tag,
                                    'process_id': self.id,
                                }
                                if tag.lower() == 'sequenceflow':
                                    data['source_ref'] = element.attrib.get('sourceRef')
                                    data['target_ref'] = element.attrib.get('targetRef')

                                element_ids.append(
                                    (1, self.element_ids.filtered(lambda x: x.bpmn_id == element.attrib.get('id')).id, data))
                for element in self.element_ids:
                    if element.bpmn_id not in new_bpmn_elements:
                        element_ids.append((2, element.id))
                vals['element_ids'] = element_ids
            except Exception as e:
                raise UserError(_('Invalid XML: %s' % e))
            print(self.element_ids)
        return super(BPMProcess, self).write(vals)
