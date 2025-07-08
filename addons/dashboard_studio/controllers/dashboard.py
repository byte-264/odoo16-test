from odoo.addons.web.controllers import export
import json
import logging
from werkzeug.exceptions import InternalServerError
from odoo import http
from odoo.http import content_disposition, request

_logger = logging.getLogger(__name__)


class DashboardExporter(export.ExcelExport):

    # @http.route('/web/dashboard/xlsx', type='http', auth="user")
    # # @serialize_exception
    # def test(self, data):
    #     params = json.loads(data)
    #     response_data = self.from_data(params['data']['labels'], params['data']['rows'])
    #     return request.make_response(response_data,
    #                                  headers=[('Content-Disposition', content_disposition(params['file_name'])),
    #                                           ('Content-Type', self.content_type)],
    #                                  cookies={'fileToken': token})

    @http.route('/web/dashboard/xlsx', type='http', auth="user")
    def index(self, data):
        try:
            params = json.loads(data)
            response_data = self.from_data(params['data']['labels'], params['data']['rows'])
            return self.base(response_data)
        except Exception as exc:
            _logger.exception("Exception during request handling.")
            payload = json.dumps({
                'code': 200,
                'message': "Odoo Server Error",
                'data': http.serialize_exception(exc)
            })
            raise InternalServerError(payload) from exc
