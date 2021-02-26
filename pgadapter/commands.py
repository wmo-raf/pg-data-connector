import click
from pgadapter import db
from pgadapter.config import SETTINGS

PG_SERVICE_SCHEMA = SETTINGS.get("PG_SERVICE_SCHEMA")
TILESERV_ROLE_PASSWORD = SETTINGS.get("TILESERV_ROLE_PASSWORD")
import logging


@click.command(name="setup_db")
def setup_db():
    logging.info("[DBSETUP]: Setting up db")
    sql = f"""DO
            $do$
            BEGIN
                CREATE EXTENSION IF NOT EXISTS postgis;
                CREATE SCHEMA IF NOT EXISTS {PG_SERVICE_SCHEMA};
               IF NOT EXISTS (
                  SELECT FROM pg_catalog.pg_roles
                  WHERE  rolname = 'tileserv') THEN
                  CREATE ROLE tileserv LOGIN ENCRYPTED PASSWORD '{TILESERV_ROLE_PASSWORD}';
                  GRANT USAGE ON SCHEMA {PG_SERVICE_SCHEMA} TO tileserv;
                  ALTER DEFAULT PRIVILEGES IN SCHEMA {PG_SERVICE_SCHEMA} GRANT SELECT ON TABLES TO tileserv;
               END IF;
            END
            $do$;"""

    db.session.execute(sql)

    db.session.commit()

    logging.info("[DBSETUP]: Done Setting up db")
