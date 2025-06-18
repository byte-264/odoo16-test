from odoo import api, SUPERUSER_ID


def _recompute_okr_node_result(env):
    failed_nodes = env['okr.node'].search([('result', '=', 'failed')])
    failed_nodes._compute_result()


def migrate(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _recompute_okr_node_result(env)
