import asyncio
import enum
import os.path
from pathlib import Path


class DataField(enum.Enum):
    SPORT_SCHEDULE_PHOTO_FILE_ID = "SPORT_SCHEDULE_PHOTO_FILE_ID"
    IS_ENABLED_NOTIFICATIONS_FETCH = "IS_ENABLED_NOTIFICATIONS_FETCH"
    IS_ENABLED_BACKEND_HEALTH_CHECK = "IS_ENABLED_BACKEND_HEALTH_CHECK"


class DataService:
    __data_file = os.path.join("save", "app.dat")
    __data: dict[str, str]
    __fields = [DataField.SPORT_SCHEDULE_PHOTO_FILE_ID.value,
                DataField.IS_ENABLED_NOTIFICATIONS_FETCH.value, DataField.IS_ENABLED_BACKEND_HEALTH_CHECK.value]

    def __init__(self):
        asyncio.run(self.__read_data())

    async def __read_data(self):
        Path(self.__data_file).parent.mkdir(parents=True, exist_ok=True)
        if os.path.exists(self.__data_file):
            with open(self.__data_file, "r") as f:
                self.__data = dict(map(lambda x: x.strip().split("=", maxsplit=1), f.readlines()))
                await self.__check_data()
                return

        self.__data = dict(map(lambda x: (x, ""), self.__fields))
        await self.__save_data()

    async def get_data(self, key) -> str:
        return self.__data.get(key)

    async def set_data(self, key, value):
        self.__data[key] = value
        await self.__save_data()

    async def clear_data(self, key):
        self.__data[key] = ""
        await self.__save_data()

    async def __save_data(self):
        with open(self.__data_file, "w+") as f:
            f.writelines("\n".join(list(map(lambda item: f"{item[0]}={item[1]}", self.__data.items()))))

    async def __check_data(self):
        self.__data = dict(map(lambda x: (x, None), self.__fields)) | self.__data
        if any(map(lambda x: x is None, self.__data.values())):
            for k, v in self.__data.items():
                if v is None:
                    self.__data[k] = ""
            await self.__save_data()


data_service = DataService()
