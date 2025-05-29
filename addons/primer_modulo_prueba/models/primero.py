from odoo import models, fields

class Primero(models.Model):
    _name = 'mi.modelo.primero'
    _description = 'Primero'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
