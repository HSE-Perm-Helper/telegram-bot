import threading
import time

from util.logs_utils import send_logs_to_admins
from util.utils import get_request


class BackendCheckHealthWorker(threading.Thread):
    def __init__(self):
        super().__init__()

    def check_health(self):
        try:
            events_response = get_request(path="/notifications")
            if events_response.status_code != 200:
                send_logs_to_admins("Проблема с бэкэндом, требуется срочно проверить его работу!")
        except Exception as e:
            send_logs_to_admins("Проблема с бэкэндом, требуется срочно проверить его работу!")

    def run(self):
        while True:
            self.check_health()
            time.sleep(300)
