from exception.service_unavailable_exception import ServiceUnavailableException


class ScheduleServiceUnavailableException(ServiceUnavailableException):
    def __init__(self):
        super().__init__("Получения расписания")