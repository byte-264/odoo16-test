from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    okr_node_ids = fields.Many2many('okr.node', 'okr_node_project_rel', 'project_id', 'node_id', string="OKR", readonly=True,
                                    help="Store all the objectives and key results related to this project.")
    okr_nodes_count = fields.Integer('Project Task', compute='_compute_okr_nodes_count')

    def _compute_okr_nodes_count(self):
        okr_nodes_data = {}
        if self.ids:
            self.env.cr.execute(
                '''
                SELECT project_id, count(node_id)
                FROM okr_node_project_rel
                WHERE project_id IN %s
                GROUP BY project_id
                ''',
                [tuple(self.ids)]
            )
            okr_nodes_data = dict(self.env.cr.fetchall())  # {id: count}
        for r in self:
            r.okr_nodes_count = okr_nodes_data.get(r.id, 0)

    def action_view_okr_nodes(self):
        action = self.env['ir.actions.act_window']._for_xml_id('to_okr.okr_node_action')
        action['domain'] = [('project_ids', 'in', self.ids)]
        return action
