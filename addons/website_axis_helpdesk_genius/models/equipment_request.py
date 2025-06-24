from odoo import api, fields, models


class EquipmentRequest(models.Model):
    _name = "equipment.request"

    ticket_id = fields.Many2one("axis.helpdesk.ticket", string="Support Ticket")
    created_by = fields.Many2one("res.users", string="Created By", default=lambda self: self.env.user)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id)
    created_on = fields.Date(string="Created On", default=fields.Date.today())
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    department_id = fields.Many2one('hr.department', string="Department")
    project_id = fields.Many2one('project.project', string="Project")
    helpdesk_team_id = fields.Many2one("axis.helpdesk.ticket.team", string="Helpdesk Team")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('equipment_received', 'Equipment Received'),
        ('equipment_returned', 'Equipment Returned'),
    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    equipment_request_line_ids = fields.One2many(
        "equipment.request.line",
        "equipment_request_id",
        string="Equipment Request Lines",
    )
    request_reason = fields.Text('Request Reason', help="Enter The Reason For Request Here.")
    internal_note = fields.Text('Internal Note', help="Enter The Reason For Request Here.")
    

    def name_get(self):
        result = []
        for equipment in self:
            name = "Equipment Request %s" % equipment.id
            result.append((equipment.id, name))
        return result

    def action_confirm(self):
        self.state = 'confirmed'

    def action_receive_equipment(self):
        self.state = 'equipment_received'

    def action_return_equipment(self):
        self.state = 'equipment_returned'


class EquipmentRequestLine(models.Model):
    _name = "equipment.request.line"
    _description = "Equipment Request Line"

    equipment_request_id = fields.Many2one(
        "equipment.request",
        string="Equipment Request",
        ondelete="cascade",
        required=True,
    )
    equipment_id = fields.Many2one(
        "maintenance.equipment",
        string="Equipment",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
    )
    description = fields.Text(string="Description")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    quantity = fields.Float(string="Quantity", default=1.0)
    uom_id = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
        required=True,
    )
