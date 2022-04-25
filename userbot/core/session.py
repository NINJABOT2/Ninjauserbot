import sys

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ..Config import Config
from .client import NinjaClient

__version__ = "1.10.6"

loop = None

if Config.Ninja_STRING:
    session = StringSession(str(Config.Ninja_STRING))
else:
    session = "NinjaUserBot"

try:
    Ninja = NinjaClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"Ninja_STRING - {e}")
    sys.exit()

Ninja.tgbot = tgbot = NinjaClient(
    session="NinjaTgbot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.BOT_TOKEN)
