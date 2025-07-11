#
# (c) Copyright Ascensio System SIA 2024
#

import json
import logging
import re
import string
from mimetypes import guess_type
from urllib.request import urlopen

import markupsafe
from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.onlyoffice_odoo.utils import config_utils, file_utils, jwt_utils, url_utils

_logger = logging.getLogger(__name__)
_mobile_regex = r"android|avantgo|playbook|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino"  # noqa: E501


class Onlyoffice_Connector(http.Controller):
    @http.route("/onlyoffice/editor/get_config", auth="user", methods=["POST"], type="json", csrf=False)
    def get_config(self, document_id=None, attachment_id=None, access_token=None):
        document = None
        if document_id:
            document = request.env["documents.document"].browse(int(document_id))
            attachment_id = document.attachment_id.id

        attachment = self.get_attachment(attachment_id)
        if not attachment:
            return request.not_found()

        attachment.validate_access(access_token)

        if attachment.res_model == "documents.document" and not document:
            document = request.env["documents.document"].browse(int(attachment.res_id))

        if document:
            self._check_document_access(document)

        data = attachment.read(["id", "checksum", "public", "name", "access_token"])[0]
        filename = data["name"]

        can_read = attachment.check_access_rights("read", raise_exception=False) and file_utils.can_view(filename)

        if not can_read:
            raise Exception("cant read")

        can_write = attachment.check_access_rights("write", raise_exception=False) and file_utils.can_edit(filename)

        config = self.prepare_editor_values(attachment, access_token, can_write)
        return config

    @http.route("/onlyoffice/file/content/test.txt", auth="public")
    def get_test_file(self):
        content = "test"
        headers = [
            ("Content-Length", len(content)),
            ("Content-Type", "text/plain"),
            ("Content-Disposition", "attachment; filename=test.txt"),
        ]
        response = request.make_response(content, headers)
        return response

    @http.route("/onlyoffice/file/content/<int:attachment_id>", auth="public")
    def get_file_content(self, attachment_id, oo_security_token=None, access_token=None):
        attachment = self.get_attachment(attachment_id, self.get_user_from_token(oo_security_token))
        if not attachment:
            return request.not_found()

        attachment.validate_access(access_token)
        attachment.check_access_rights("read")

        if jwt_utils.is_jwt_enabled(request.env):
            token = request.httprequest.headers.get(config_utils.get_jwt_header(request.env))
            if token:
                token = token[len("Bearer ") :]

            if not token:
                raise Exception("expected JWT")

            jwt_utils.decode_token(request.env, token)

        stream = request.env["ir.binary"]._get_stream_from(attachment, "datas", None, "name", None)

        send_file_kwargs = {"as_attachment": True, "max_age": None}

        return stream.get_response(**send_file_kwargs)

    @http.route("/onlyoffice/editor/<int:attachment_id>", auth="public", type="http", website=True)
    def render_editor(self, attachment_id, access_token=None):
        attachment = self.get_attachment(attachment_id)
        if not attachment:
            return request.not_found()

        attachment.validate_access(access_token)

        if attachment.res_model == "documents.document":
            document = request.env["documents.document"].browse(int(attachment.res_id))
            self._check_document_access(document)

        data = attachment.read(["id", "checksum", "public", "name", "access_token"])[0]
        filename = data["name"]

        can_read = attachment.check_access_rights("read", raise_exception=False) and file_utils.can_view(filename)
        can_write = attachment.check_access_rights("write", raise_exception=False) and file_utils.can_edit(filename)

        if not can_read:
            raise Exception("cant read")

        return request.render(
            "onlyoffice_odoo.onlyoffice_editor", self.prepare_editor_values(attachment, access_token, can_write)
        )

    @http.route(
        "/onlyoffice/editor/callback/<int:attachment_id>", auth="public", methods=["POST"], type="http", csrf=False
    )
    def editor_callback(self, attachment_id, oo_security_token=None, access_token=None):
        response_json = {"error": 0}

        try:
            body = request.get_json_data()

            attachment = self.get_attachment(attachment_id, self.get_user_from_token(oo_security_token))
            if not attachment:
                raise Exception("attachment not found")

            attachment.validate_access(access_token)
            attachment.check_access_rights("write")

            if jwt_utils.is_jwt_enabled(request.env):
                token = body.get("token")

                if not token:
                    token = request.httprequest.headers.get(config_utils.get_jwt_header(request.env))
                    if token:
                        token = token[len("Bearer ") :]

                if not token:
                    raise Exception("expected JWT")

                body = jwt_utils.decode_token(request.env, token)
                if body.get("payload"):
                    body = body["payload"]

            status = body["status"]

            if (status == 2) | (status == 3):  # mustsave, corrupted
                file_url = url_utils.replace_public_url_to_internal(request.env, body.get("url"))
                attachment.write({"raw": urlopen(file_url, timeout=30).read(), "mimetype": guess_type(file_url)[0]})

        except Exception as ex:
            response_json["error"] = 1
            response_json["message"] = http.serialize_exception(ex)

        return request.make_response(
            data=json.dumps(response_json),
            status=500 if response_json["error"] == 1 else 200,
            headers=[("Content-Type", "application/json")],
        )

    def prepare_editor_values(self, attachment, access_token, can_write):
        data = attachment.read(["id", "checksum", "public", "name", "access_token"])[0]
        key = str(data["id"]) + str(data["checksum"])
        docserver_url = config_utils.get_doc_server_public_url(request.env)
        odoo_url = config_utils.get_base_or_odoo_url(request.env)

        filename = self.filter_xss(data["name"])

        security_token = jwt_utils.encode_payload(
            request.env, {"id": request.env.user.id}, config_utils.get_internal_jwt_secret(request.env)
        )
        security_token = security_token.decode("utf-8") if isinstance(security_token, bytes) else security_token
        access_token = access_token.decode("utf-8") if isinstance(access_token, bytes) else access_token
        path_part = (
            str(data["id"])
            + "?oo_security_token="
            + security_token
            + ("&access_token=" + access_token if access_token else "")
            + "&shardkey="
            + key
        )

        document_type = file_utils.get_file_type(filename)

        is_mobile = bool(re.search(_mobile_regex, request.httprequest.headers.get("User-Agent"), re.IGNORECASE))

        root_config = {
            "width": "100%",
            "height": "100%",
            "type": "mobile" if is_mobile else "desktop",
            "documentType": document_type,
            "document": {
                "title": filename,
                "url": odoo_url + "onlyoffice/file/content/" + path_part,
                "fileType": file_utils.get_file_ext(filename),
                "key": key,
                "permissions": {"edit": can_write},
            },
            "editorConfig": {
                "mode": "edit" if can_write else "view",
                "lang": request.env.user.lang,
                "user": {"id": str(request.env.user.id), "name": request.env.user.name},
                "customization": {},
            },
        }

        if can_write:
            root_config["editorConfig"]["callbackUrl"] = odoo_url + "onlyoffice/editor/callback/" + path_part

        if jwt_utils.is_jwt_enabled(request.env):
            root_config["token"] = jwt_utils.encode_payload(request.env, root_config)

        return {
            "docTitle": filename,
            "docIcon": f"/onlyoffice_odoo/static/description/editor_icons/{document_type}.ico",
            "docApiJS": docserver_url + "web-apps/apps/api/documents/api.js",
            "editorConfig": markupsafe.Markup(json.dumps(root_config)),
        }

    def get_attachment(self, attachment_id, user=None):
        IrAttachment = request.env["ir.attachment"]
        if user:
            IrAttachment = IrAttachment.with_user(user)
        try:
            return IrAttachment.browse([attachment_id]).exists().ensure_one()
        except Exception:
            return None

    def get_user_from_token(self, token):
        if not token:
            raise Exception("missing security token")

        user_id = jwt_utils.decode_token(request.env, token, config_utils.get_internal_jwt_secret(request.env))["id"]
        user = request.env["res.users"].sudo().browse(user_id).exists().ensure_one()
        return user

    def filter_xss(self, text):
        allowed_symbols = set(string.ascii_letters + string.digits + " _-,.:@+")
        text = "".join(char for char in text if char in allowed_symbols)

        return text

    def _check_document_access(self, document):
        if document.is_locked and document.lock_uid.id != request.env.user.id:
            _logger.error("Document is locked by another user")
            raise Forbidden()
        try:
            document.check_access_rule("read")
        except AccessError as e:
            _logger.error("User has no read access rights to open this document")
            raise Forbidden() from e
