import os

from util.utils import parse_boolean

x_secret_key = os.getenv("x_secret_key")
bot_token = os.getenv("bot_token")
base_url = os.getenv("base_url")
front_base_url = os.getenv("front_base_url")
is_prod = parse_boolean(os.getenv("is_prod"))

if is_prod:
    RD_HOST = os.getenv("RD_HOST")
    RD_PORT = os.getenv("RD_PORT")
