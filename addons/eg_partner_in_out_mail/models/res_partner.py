from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    total_in_mail = fields.Integer(string="Incoming", compute="_compute_total_partner_mail")
    total_out_mail = fields.Integer(string="Outgoing", compute="_compute_total_partner_mail")

    def _compute_total_partner_mail(self):
        for partner_id in self:
            partner_id.total_in_mail = len(self.env["mail.mail"].search([("author_id", "=", partner_id.id)]))
            partner_id.total_out_mail = len(self.env["mail.mail"].search([("recipient_ids", "in", partner_id.id)]))

    def action_view_partner_in_mail(self):
        self.ensure_one()
        action = self.env.ref('mail.action_view_mail_mail')
        tree_view_id = self.env.ref('mail.view_mail_tree')
        form_view_id = self.env.ref('mail.view_mail_form')
        mail_ids = self.env["mail.mail"].search([("author_id", "=", self.id)])
        return {
            'name': action.name,
            'type': action.type,
            'view_mode': action.view_mode,
            'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('id', 'in', mail_ids.ids)],

        }

    def action_view_partner_out_mail(self):
        self.ensure_one()
        action = self.env.ref('mail.action_view_mail_mail')
        tree_view_id = self.env.ref('mail.view_mail_tree')
        form_view_id = self.env.ref('mail.view_mail_form')
        mail_ids = self.env["mail.mail"].search([("recipient_ids", "in", self.id)])
        return {
            'name': action.name,
            'type': action.type,
            'view_mode': action.view_mode,
            'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('id', 'in', mail_ids.ids)],
        }