from odoo import models, fields, api

class ProcessInstance(models.Model):
    _name = 'bpm.process.instance'
    _description = 'Process Instance'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    process_id = fields.Many2one('bpm.process', string='Process', required=True, readonly=True)
    state = fields.Selection([
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('terminated', 'Terminated'),
    ], string='State', copy=False, default='in_process', required=True,
        compute = '_compute_state',readonly=False)

    res_model_id = fields.Many2one('ir.model', related='process_id.res_model_id', string='Model', readonly=True)
    model_name = fields.Char(related='process_id.model_name', string='Model Name', readonly=True)
    res_id = fields.Integer(string='Record ID', readonly=True)
    task_ids = fields.One2many('project.task', 'process_instance_id', string='Tasks', readonly=True)
    process_element_ids = fields.One2many('bpm.process.instance.element', 'instance_id', string='Elements', readonly=True)

    context = fields.Text(string='Context', readonly=True)

    @api.depends('task_ids')
    def _compute_state(self):
        for rec in self:
            if rec.task_ids.filtered(lambda x: x.process_step_id):
                rec.state = 'in_progress'
            else:
                rec.state = 'done'

    @api.depends('process_id', 'create_date')
    def _compute_name(self):
        for rec in self:
            rec.name = '%s - %s' % (rec.process_id.name, rec.create_date)


class ProcessInstanceElement(models.Model):
    _name = 'bpm.process.instance.element'
    _description = 'Process Instance Element'

    name = fields.Char(string='Name', related='element_id.name', store=True)
    instance_id = fields.Many2one('bpm.process.instance', string='Process Instance',ondelete='cascade', readonly=True)
    element_id = fields.Many2one('bpm.process.element', string='Process Element', readonly=True)
    date_start = fields.Datetime(string='Start Date', default=fields.Datetime.now, readonly=True)
    type = fields.Char(related='element_id.type', string='Type', store=True)

