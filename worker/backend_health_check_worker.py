import asyncio

from util.logs_utils import send_logs_to_admins
from api.utils import get_request


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
            await self.check_health()
            await asyncio.sleep(300)
