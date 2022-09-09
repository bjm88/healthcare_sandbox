from app.api import application
from . import medical_notes_api
from datetime import timedelta
from flask import Flask, session, redirect, url_for, request, jsonify, abort, g
from flask_cors import CORS
from markupsafe import escape
from ..common.database_utils import DatabaseManager
from ..common import settings
from flask_caching import Cache

@application.before_request
def setup_database_session():
    g.db_session = DatabaseManager.get_db_session()


@application.errorhandler(Exception)
def rollback_database_session(exception):
    g.db_session.rollback()
    raise exception


@application.after_request
def close_database_session(response):
    try:
        g.db_session.commit()
    finally:
        g.db_session.close()
        return response


cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(application)


@application.route("/")
def status():
    return "Welcome to the Health Sandbox API.  The API service is running normallly."




allowed_origins = [
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1",
    "http://127.0.0.1",
    "http://localhost:3000",
    "http://localhost:5001",
    "http://localhost",
    "http://healthsandboxc-api-dev.healthsandbox.org:5001",
    "http://healthsandboxc-api-dev.healthsandbox.org",
    "http://healthsandboxc-api-test.healthsandbox.org",
    "http://healthsandboxc-api.healthsandbox.org",
]


@application.before_request
def check_login_if_secure_path():
    userType = session.get("userType", None)
    user_id = session.get("userId", None)

    #g.current_user = current_user
    # check user logged in
    if request.path.startswith("/api/s/") and request.method.lower() != "options":
        user_id = session.get("userId", None)
        if user_id is None:
            return abort(401)

    # CHECK USER PERMISSION TO ACCESS THESE URLS
    if request.path.startswith("/api/s/console") and request.method.lower() != "options":

        # TODO check user is admin/roles permissions
        print("TODO secure console apis")

    if request.path.startswith("/api/webhook/") and request.method.lower() != "options":
        authSecret = request.headers.get("AuthSecret", None)
        if authSecret is None or len(authSecret) < 1:
            authSecret = request.args.get("AuthSecret", None)

        if authSecret is None or len(authSecret) < 1 or authSecret != settings.EXTERNAL_WEBHOOK_SECRET:
            print(
                "Invalid webhook call to "
                + str(request.path)
                + ", bad HTTP Header AuthSecret: invalid: "
                + str(authSecret)
            )
            return abort(401)

    if request.path.startswith("/api/oauth/s/") and request.method.lower() != "options":
        oauthAccessToken = request.headers.get("Authorization", None)
        if oauthAccessToken is None or len(oauthAccessToken) < 1:
            print(
                "Invalid OAuth call to Secured OAuth endpoint, bad HTTP Header Bearer token missing")
            return abort(401)

    # check for browser's Origin and if sent ensure its a valid domain or abort request
    # note browsers will block the response and content with their SAME ORIGIN POLICY
    # however for CSRF attacks the POST or GET data processing could still happen without this on back end
    if "Origin" in request.headers:
        if not request.headers["Origin"] in allowed_origins:
            print("Invalid CORS call, aborting processing from Origin " +
                  str(request.headers["Origin"]))
            return abort(403)

    # ensure activity updates session expiration on each call, pushing back the timeout
    session.permanent = True
    application.permanent_session_lifetime = timedelta(hours=8)
    session.modified = True
    # print("Session time is updated for next 1 hour {}".format(datetime.datetime.now()))


@application.after_request
def add_headers(response):
    # print("evaluating headers for orgin " + request.headers['Origin'])
    if "Origin" in request.headers and request.headers["Origin"] in allowed_origins:
        # print("adding headers for orgin " + request.headers['Origin'])
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Origin",
                             request.headers["Origin"])
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, Origin, X-Requested-With, Accept, x-auth, Set-Cookie,content-length,content-type,accept-encoding,accept-language,accept",
        )
        response.headers.add(
            "Access-Control-Expose-Headers", "Content-Type,Content-Length,Authorization,X-Pagination, Set-Cookie"
        )

    # security headers, dont remove
    response.headers.add("strict-transport-security",
                         "max-age=63072000; includeSubdomains; preload")
    response.headers.add("x-xss-protection", "1; mode=block")
    response.headers.add("content-security-policy",
                         "frame-ancestors 'self' *.atlantichealth.org atlantichealth.org")
    response.headers.add("x-content-type-options", "nosniff")
    response.headers.add("referrer-policy", "origin")
    response.headers.add(
        "feature-policy", "camera *; microphone *; geolocation 'self'")
    response.headers.add("permissions-policy",
                         "camera=*, microphone=*, geolocation=*")

    return response


if __name__ == "__main__":
    application.secret_key = settings.SECRET_KEY

    #sess.init_app(app)
    application.debug = application.config.get("ENVIRONMENT") != "production"
    application.run(host="0.0.0.0", port=5001, debug=True)
