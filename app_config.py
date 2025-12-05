import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from config import settings


@dataclass
class DatabaseConfig:
    database_url: str
    engine_options: Dict[str, Any]
    connector: Optional[object] = None


def load_base_config(app, logger: logging.Logger) -> None:
    """Apply non-database Flask configuration."""
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET")
    if not app.config["SECRET_KEY"]:
        raise ValueError("SESSION_SECRET environment variable must be set")

    app.config["SERVER_NAME"] = None
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"

    app.config["GOOGLE_MAPS_API_KEY"] = settings.get("GOOGLE_MAPS_API_KEY", required=True)
    if not app.config["GOOGLE_MAPS_API_KEY"]:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable must be set")

    def _get_float(key: str, default: float) -> float:
        try:
            value = settings.get(key)
            return float(value) if value else default
        except (TypeError, ValueError):
            return float(default)

    app.config["MAP_BOUNDS_NORTH"] = _get_float("MAP_BOUNDS_NORTH", 49.0)
    app.config["MAP_BOUNDS_SOUTH"] = _get_float("MAP_BOUNDS_SOUTH", 45.5)
    app.config["MAP_BOUNDS_WEST"] = _get_float("MAP_BOUNDS_WEST", -124.8)
    app.config["MAP_BOUNDS_EAST"] = _get_float("MAP_BOUNDS_EAST", -116.9)

    logger.debug("Base configuration loaded")


def prepare_database_config(logger: logging.Logger) -> DatabaseConfig:
    """Build database URL and engine options, supporting Cloud SQL connector."""
    engine_options: Dict[str, Any] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
    }

    use_cloud_sql_connector = settings.get_bool("USE_CLOUD_SQL_CONNECTOR", False)
    connector = None

    if use_cloud_sql_connector:
        try:
            import pg8000.dbapi  # type: ignore
            from google.cloud.sql.connector import Connector, IPTypes  # type: ignore
        except ImportError as import_error:
            raise RuntimeError(
                "USE_CLOUD_SQL_CONNECTOR is enabled but required dependencies are missing. "
                "Install cloud-sql-python-connector[pg8000] and pg8000."
            ) from import_error

        connector = Connector()

        instance_connection_name = settings.get("INSTANCE_CONNECTION_NAME") or settings.get("CLOUD_SQL_INSTANCE")
        db_user = settings.get("POSTGRES_USER") or settings.get("PGUSER")
        db_name = settings.get("POSTGRES_DB") or settings.get("PGDATABASE")
        enable_iam_auth = settings.get_bool("CLOUD_SQL_ENABLE_IAM_AUTH", False)
        db_password = None if enable_iam_auth else (settings.get("POSTGRES_PASSWORD") or settings.get("PGPASSWORD"))
        ip_type_setting = (settings.get("CLOUD_SQL_IP_TYPE") or "PUBLIC").upper()
        ip_type = IPTypes.PRIVATE if ip_type_setting == "PRIVATE" else IPTypes.PUBLIC

        missing = [
            name
            for name, value in [
                ("INSTANCE_CONNECTION_NAME", instance_connection_name),
                ("POSTGRES_USER/PGUSER", db_user),
                ("POSTGRES_DB/PGDATABASE", db_name),
            ]
            if not value
        ]
        if not enable_iam_auth and not db_password:
            missing.append("POSTGRES_PASSWORD/PGPASSWORD")
        if missing:
            raise ValueError(f"Missing required Cloud SQL settings: {', '.join(missing)}")

        def get_conn() -> pg8000.dbapi.Connection:
            return connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_password,
                db=db_name,
                enable_iam_auth=enable_iam_auth,
                ip_type=ip_type,
            )

        engine_options["creator"] = get_conn
        database_url = "postgresql+pg8000://"
        logger.info(
            "Using Cloud SQL Python Connector for database connections (ip_type=%s, iam_auth=%s)",
            ip_type_setting,
            enable_iam_auth,
        )
    else:
        database_url = settings.get("DATABASE_URL")

        if database_url and database_url.startswith("sqlite://"):
            logger.info("Detected old SQLite DATABASE_URL, attempting to construct PostgreSQL URL from environment variables")
            pg_user = os.environ.get("PGUSER")
            pg_password = os.environ.get("PGPASSWORD")
            pg_host = os.environ.get("PGHOST")
            pg_port = os.environ.get("PGPORT", "5432")
            pg_database = os.environ.get("PGDATABASE")

            if all([pg_user, pg_password, pg_host, pg_database]):
                database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
                logger.info("Constructed PostgreSQL DATABASE_URL from environment variables")
            else:
                logger.warning("SQLite URL detected but cannot construct PostgreSQL URL (missing PG* env vars)")

        if not database_url:
            raise ValueError("DATABASE_URL environment variable must be set")
        if not database_url.startswith("postgresql"):
            raise ValueError("DATABASE_URL must use a PostgreSQL driver (postgresql scheme required)")

    return DatabaseConfig(database_url=database_url, engine_options=engine_options, connector=connector)


__all__ = ["DatabaseConfig", "load_base_config", "prepare_database_config"]
