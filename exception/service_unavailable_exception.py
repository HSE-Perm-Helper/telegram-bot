from message import common_messages


class ServiceUnavailableException(Exception):
    service: str

    def __init__(self, service: str):
        self.service = service
        super().__init__(f'Service {service} is Unavailable')

    def __str__(self):
        return common_messages.SERVICE_UNAVAILABLE_EXCEPTION.format(service=self.service.lower())
