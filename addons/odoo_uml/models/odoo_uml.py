
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging

from lxml import etree

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from mako.template import Template
from mako.runtime import Context
from odoo.tools.safe_eval import safe_eval
from io import StringIO
import logging

from .utils.odoo_uml import PackageDiagram, InvPackageDiagram, ClassDiagram
from .utils.plant_uml import PlantUMLClassDiagram, italic, bold

_logger = logging.getLogger(__name__)


class OdooUML(models.TransientModel):
    _name = 'odoo.uml'
    _description = 'OdooUML'

    module = fields.Many2one(
        comodel_name='ir.module.module',
        string='Module',
        required=False)



    puml_dependency_diagram_png = fields.Binary(
        string=u'Dependency Diagram Image',
        help='Dependency diagram as encode base64 PNG image.',
        related="module.puml_dependency_diagram_png"
    )

    # Inverse Dependency

    puml_inv_dependency_diagram_png = fields.Binary(
        string=u'Inverse Dependency Diagram Image',
        help='Dependency diagram as encode base64 PNG image.',
        related="module.puml_inv_dependency_diagram_png"
    )

    # *************************************************************************
    # Class Diagrams
    # *************************************************************************

    # Class Diagram


    puml_class_diagram_png = fields.Binary(
        string=u'Class Diagram Image',
        help='Class diagram as encode base64 PNG image.',
        related="module.puml_class_diagram_png"
    )



