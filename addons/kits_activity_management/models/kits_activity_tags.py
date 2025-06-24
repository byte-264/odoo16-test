from odoo import _,models,fields

class kits_activity_tags(models.Model):
    _name = 'kits.activity.tags'
    _description = "Activity Tags"

    name = fields.Char("Name")