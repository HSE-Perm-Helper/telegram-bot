import asyncio

from api.utils import get_request
from data.data_service import DataField, data_service
from util.logs_utils import send_logs_to_admins
from util.utils import parse_boolean


class BackendCheckHealthWorker:
    def __init__(self):
        super().__init__()

    async def check_health(self):
        try:
            events_response = await get_request(path="/v2/notifications")
            if events_response.status_code != 200:
                await send_logs_to_admins("Проблема с бэкэндом, требуется срочно проверить его работу!")
        except Exception as e:
            await send_logs_to_admins("Проблема с бэкэндом, требуется срочно проверить его работу!")

    async def run(self):
        while True:
            if parse_boolean(await data_service.get_data(DataField.IS_ENABLED_BACKEND_HEALTH_CHECK.value)):
                await self.check_health()
            await asyncio.sleep(300)
