import logging
import os
from datetime import timedelta
from typing import Final

# enviroment
ENVIRONMENT: Final = os.getenv("HS_ENV", "dev")
LOGGING_LEVEL: Final = logging.DEBUG if ENVIRONMENT != "production" else logging.INFO

#encryption and secrets
SECRET_KEY: Final = os.getenv("HC_SESSION_SECRET", "healthsandbox123!")

# Database
DB_HOST: Final = os.getenv("RDS_HOSTNAME", "localhost")
DB_PORT: Final = os.getenv("RDS_PORT", "5432")
DB_NAME: Final = os.getenv("RDS_DB_NAME", "healthsandbox")
DB_USERNAME: Final = os.getenv("RDS_USERNAME", "healthsandbox")
DB_PASSWORD: Final = os.getenv("RDS_PASSWORD", "")

# AWS common
AWS_DEFAULT_REGION: Final = os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
AWS_ACCESS_KEY_ID: Final = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: Final = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
