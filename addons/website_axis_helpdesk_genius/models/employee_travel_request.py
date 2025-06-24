from odoo import models, fields, api


class EmployeeTravelRequest(models.Model):

    _name = 'employee.travel.request'
    _description = 'Employee Travel Reques For Helpdesk'

    name = fields.Char(string="Request Number", required=True)
    helpdesk_ticket_id = fields.Many2one("axis.helpdesk.ticket", string="Helpdesk Ticket")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    manager_id = fields.Many2one("hr.employee", string="Manager")
    company_id = fields.Many2one("res.company", string="Company")
    request_by_id = fields.Many2one("res.users", string="Request By", default=lambda self: self.env.user)
    confirm_by_id = fields.Many2one("res.users", string="Confirm By")
    approved_by_id = fields.Many2one("res.users", string="Approved By")
    helpdesk_support_id = fields.Many2one("res.users", string="Helpdesk Support")
    department_id = fields.Many2one("hr.department", string="Department")
    job_position_id = fields.Many2one("hr.job", string="Job Position")
    currency_id = fields.Many2one("res.currency", string="Currency")
    request_date = fields.Date(string="Request Date")
    confirm_date = fields.Date(string="Confirm Date")
    approved_date = fields.Date(string="Approved Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('rejected', 'Rejected')],
        string="Status", default='draft', track_visibility='onchange')
    travel_purpose = fields.Char(string="Travel Purpose")
    project_id = fields.Many2one("project.project", string="Project")
    analytic_account_id = fields.Many2one("account.analytic.account", string="Analytic Account")
    # from_location = fields.Char(string="Travel From")
    # to_location = fields.Char(string="Travel To")
    req_departure_date = fields.Date(string="Request Departure Date")
    req_return_date = fields.Date(string="Request Return Date")
    req_mode_of_travel_days = fields.Char(string="Request Mode Of Travel")
    travel_days = fields.Char(string="Days Of Travel")
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email")
    available_departure_date = fields.Date(string="Available Departure Date")
    available_return_date = fields.Date(string="Available Return Date")
    departure_mode_of_travel = fields.Char(string="Departure Mode Of Travel")
    return_mode_of_travel = fields.Char(string="Return Mode Of Travel")
    visa_agent = fields.Char(string="Visa Agent")
    ticket_booking_agent = fields.Char(string="Ticket Booking Agent")
    bank_name = fields.Char(string="Bank Name")
    cheque_number = fields.Char(string="Cheque Number")
    expense_line_ids = fields.One2many("employee.travel.expense.line", "travel_request_id", string="Expense Lines")
    from_location_id = fields.Many2one('travel.location', string="Travel From")
    to_location_id = fields.Many2one('travel.location', string="Travel To")

    def action_confirm(self):
        self.state = 'confirm'
        self.confirm_date = fields.Date.today()

    def action_reject(self):
        self.state = 'rejected'


class EmployeeTravelExpenseLine(models.Model):
    _name = 'employee.travel.expense.line'
    _description = 'Employee Travel Expense Line'

    expense_id = fields.Many2one("hr.expense", string="Expense")
    description = fields.Char(string="Description")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity")
    uom_id = fields.Many2one("uom.uom", string="UOM")
    currency_id = fields.Many2one("res.currency", string="Currency")
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)
    travel_request_id = fields.Many2one("employee.travel.request", string="Travel Request")

    @api.depends("unit_price", "quantity")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.unit_price * line.quantity
            print("THE EXPENSE LINE SUBTOTAL IS ------------------", line.subtotal)

    @api.onchange("subtotal")
    def _compute_total(self):
        for expense_line in self:
            expense_line.total = sum(line.subtotal for line in expense_line)
            print("THE EXPENSE LINE SUBTOTAL IS ------------------", expense_line.total)

# --------------------------------------------------------------------------------------------------
#                                 EXTRA CODE
#     advance_payment_request_line_ids = fields.One2many(
#         "advance.payment.request.line",
#         "travel_request_id",
#         string="Advance Payment Request Lines"
#     )
#
# class AdvancePaymentRequestLine(models.Model):
#     _name = "advance.payment.request.line"
#     _description = "Advance Payment Request Line"
#
    # travel_request_id = fields.Many2one("employee.travel.request", string="Travel Request")
    # expense = fields.Char(string="Expense")
    # description = fields.Char(string="Description")
    # unit_price = fields.Float(string="Unit Price")
    # quantity = fields.Float(string="Quantity")
    # uom_id = fields.Many2one("uom.uom", string="UOM")
    # currency_id = fields.Many2one("res.currency", string="Currency")
    # subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)
    # total = fields.Float(string="Total", compute="_compute_total", store=True)


# --------------------------------------------------------------------------------------------------
