from settings.setting_code import SettingCode


class BaseSetting:
    title: str
    code: SettingCode
    api_code: str

    def __init__(self, title: str, code: SettingCode, api_code: str):
        self.title = title
        self.code = code
        self.api_code = api_code
