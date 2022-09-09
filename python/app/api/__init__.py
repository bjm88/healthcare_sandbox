import logging
from datetime import date, time
from enum import Enum
from flask import Flask, json
from flask.json import JSONEncoder
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import HTTPException

from ..common import settings
from ..common.database_utils import DatabaseManager


try:
    DatabaseManager.get_database()
except BaseException as error:
    print("Error connecting to database : {}".format(error))


LOG = logging.getLogger(__name__)

logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format="[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s %(threadName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
)


application = Flask(__name__)
application.config.from_object(settings)

ma = Marshmallow(application)


@application.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    LOG.warning(f"<HTTPException> {e.name}: {e.description}")
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, time):
            return o.isoformat()
        elif isinstance(o, Enum):
            return o.name

        return super().default(o)


application.json_encoder = CustomJSONEncoder
