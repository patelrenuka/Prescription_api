import json
import logging
import functools
import werkzeug.wrappers

from odoo import http
from odoo.addons.Prescription.model.common_http_response import invalid_response
from odoo.exceptions import AccessDenied, AccessError
from odoo.http import request

_logger = logging.getLogger(__name__)


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        access_token = request.httprequest.headers.get("Authorization")
        
        if not access_token:
            return invalid_response("access_token_not_found", "missing access token in request header", 401)
        access_token = access_token.replace("Bearer ", "")
        print("+++++++++++++access_token",access_token)
        access_token_data = request.env["api.access_token"].sudo().search([("token", "=", access_token)],
                                                                          order="id DESC", limit=1)

        if access_token_data.find_or_create_token(user_id=access_token_data.user_id.id) != access_token:
            return invalid_response("access_token", "token seems to have expired or invalid", 401)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap


class AccessToken(http.Controller):
    @http.route("/api/login", methods=["GET"], type="http", auth="none", csrf=False)
    def api_login(self, **post):
        params = ["db", "username", "password"]
        params = {key: post.get(key) for key in params if post.get(key)}
        print("############## params db", params.get("db"))
        print("############## post usernae", post.get("password"))
        db, username, password = (
            params.get("db"),
            post.get("username"),
            post.get("password"),
        )
        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            headers = request.httprequest.headers
            db = headers.get("db")
            username = headers.get("username")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                return invalid_response(
                    "missing error", "either of the following are missing [db, username,password]", 403,
                )
        try:
            request.session.authenticate(db, username, password)
        except AccessError as aee:
            return invalid_response("Access error", "Error: %s" % aee.name)
        except AccessDenied as ade:
            return invalid_response("Access denied", "username, password or db invalid")
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return invalid_response("wrong database name", error, 403)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            return invalid_response(401, error, info)

        # Generate tokens
        access_token = request.env["api.access_token"].find_or_create_token(user_id=uid, create=True)
        return werkzeug.wrappers.Response(
            status=200,
            content_type="application/json; charset=utf-8",
            headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
            response=json.dumps(
                {
                    "uid": uid,
                    "access_token": access_token
                }
            ),
        )

    
