"""
Configuration for the GPO microservice settings.
Context is switched based on if the app is in debug mode.
"""
import json
import logging
import os

log = logging.getLogger(__name__)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG set is set to True if env var is "True"
DEBUG = os.getenv("DEBUG", "False") == "True"

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.getLevelName(logging.INFO))

GPO_USERNAME = os.getenv("GPO_USERNAME")
GPO_PASSWORD = os.getenv("GPO_PASSWORD")
GPO_HOST = os.getenv("GPO_HOST")
GPO_HOSTKEY = os.getenv("GPO_HOSTKEY")


def get_db_uri():
    """get db uri"""
    vcap_services = os.getenv("VCAP_SERVICES", "")
    try:
        db_uri = json.loads(vcap_services)["aws-rds"][0]["credentials"]["uri"]
    except (json.JSONDecodeError, KeyError) as err:
        log.warning("Unable to load db_uri from VCAP_SERVICES")
        log.debug("Error: %s", str(err))
        db_uri = ""

    # Sqlalchemy requires 'postgresql' as the protocol
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

    return os.getenv("DB_URI", db_uri)


DB_URI = get_db_uri()
SCHEMA_NAME = "gpo"
DEST_FILE_DIR = "gsa_order"
