import logging
import os
import sys
import uuid
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler

from configs import higgs_config
from higgs_app import HiggsApp

# 创建一个context variable来保存request_id
request_id_var: ContextVar[str] = ContextVar("req_id", default="none")


def init_app(app: HiggsApp):
    log_handlers: list[logging.Handler] = []
    log_file = higgs_config.LOG_FILE
    if log_file:
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        log_handlers.append(
            RotatingFileHandler(
                filename=log_file,
                maxBytes=higgs_config.LOG_FILE_MAX_SIZE * 1024 * 1024,
                backupCount=higgs_config.LOG_FILE_BACKUP_COUNT,
            )
        )

    # Always add StreamHandler to log to console
    sh = logging.StreamHandler(sys.stdout)
    log_handlers.append(sh)

    # Apply RequestIdFilter to all handlers
    for handler in log_handlers:
        handler.addFilter(RequestIdFilter())

    logging.basicConfig(
        level=higgs_config.LOG_LEVEL,
        format=higgs_config.LOG_FORMAT,
        datefmt=higgs_config.LOG_DATEFORMAT,
        handlers=log_handlers,
        force=True,
    )

    # Apply RequestIdFormatter to all handlers
    apply_request_id_formatter()

    # Disable propagation for noisy loggers to avoid duplicate logs
    logging.getLogger("sqlalchemy.engine").propagate = False
    log_tz = higgs_config.LOG_TZ
    if log_tz:
        from datetime import datetime

        import pytz

        timezone = pytz.timezone(log_tz)

        def time_converter(seconds):
            return datetime.fromtimestamp(seconds, tz=timezone).timetuple()

        for handler in logging.root.handlers:
            if handler.formatter:
                handler.formatter.converter = time_converter


def get_request_id():
    if request_id_var.get():
        return request_id_var.get()

    new_uuid = uuid.uuid4().hex[:10]
    request_id_var.set(new_uuid)

    return new_uuid


class RequestIdFilter(logging.Filter):
    # This is a logging filter that makes the request ID available for use in
    # the logging format. Note that we're checking if we're in a request
    # context, as we may want to log things before FastAPI is fully loaded.
    def filter(self, record):
        record.req_id = get_request_id() if get_request_id() else ""
        return True


class RequestIdFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "req_id"):
            record.req_id = ""
        return super().format(record)


def apply_request_id_formatter():
    for handler in logging.root.handlers:
        if handler.formatter:
            handler.formatter = RequestIdFormatter(higgs_config.LOG_FORMAT, higgs_config.LOG_DATEFORMAT)
