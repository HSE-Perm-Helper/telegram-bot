import structlog

from env import is_prod


def init_logging(instance_id: str):
    if is_prod:
        __configure_prod_logging(instance_id)
    else:
        __configure_dev_logging()


def __configure_dev_logging():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ]
    )

def __configure_prod_logging(instance_id: str):
    def add_instance_id(_, __, event_dict):
        event_dict["instance_id"] = instance_id
        return event_dict

    def add_stream_name(_, __, event_dict):
        event_dict["stream_name"] = "frontend"
        return event_dict

    def add_service_name(_, __, event_dict):
        event_dict["service_name"] = "telegram-bot"
        return event_dict

    exception_transformer = structlog.tracebacks.ExceptionDictTransformer()
    exception_format_json = structlog.processors.ExceptionRenderer(exception_transformer)

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", key="@timestamp"),
            add_instance_id,
            add_stream_name,
            add_service_name,
            structlog.contextvars.merge_contextvars,
            exception_format_json,
            structlog.processors.EventRenamer("message"),
            structlog.processors.JSONRenderer(),
        ]
    )