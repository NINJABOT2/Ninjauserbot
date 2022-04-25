import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest

from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import Ninja
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module, start_spam
from .tools import create_supergroup

LOGS = logging.getLogger("NinjaUserBot")
cmdhr = Config.HANDLER


async def setup_bot():
    """
    To set up bot for userbot
    """
    try:
        await Ninja.connect()
        config = await Ninja(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == Ninja.session.server_address:
                if Ninja.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {Ninja.session.dc_id}"
                        f" to {option.id}"
                    )
                Ninja.session.set_dc(option.id, option.ip_address, option.port)
                Ninja.session.save()
                break
        bot_details = await Ninja.tgbot.get_me()
        Config.BOT_USERNAME = f"@{bot_details.username}"
        Ninja.me = await Ninja.get_me()
        Ninja.uid = Ninja.tgbot.uid = utils.get_peer_id(Ninja.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(Ninja.me)
    except Exception as e:
        LOGS.error(f"Ninja_STRING - {e}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.NinjaUBLOGO = await Ninja.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/c5a74e1817b97a6cd3fe4.jpg",
                caption="**Your NinjaBot has been started successfully.**",
                buttons=[(Button.url("Support", "https://t.me/NinjaBot_OP"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await Ninja.check_testcases()
            message = await Ninja.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**Ok Bot is Back and Alive.**"
            await Ninja.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await Ninja.send_message(
                    msg_details[0],
                    f"{cmdhr}ping -a",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await Ninja.tgbot.get_me()
    lol = bot_details.username
    addgvar("BOT_USERNAME", lol)
    try:
        await Ninja(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=lol,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await Ninja(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[lol],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder):
    """
    To load plugins from the mentioned folder
    """
    path = f"userbot/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    type = True
                    check = 0
                    while type:
                        try:
                            load_module(
                                shortname.replace(".py", ""),
                                plugin_path=f"userbot/{folder}",
                            )
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"userbot/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"userbot/{folder}/{shortname}.py"))
                LOGS.info(f"unable to load {shortname} because of error {e}")


async def hekp():
    try:
        os.environ[
            "Ninja_STRING"
        ] = "String Is A Sensitive Data \nSo Its Protected By NinjaBot"
    except Exception as e:
        print(str(e))
    try:
        await Ninja(JoinChannelRequest("@NinjaBot_OP"))
    except BaseException:
        pass
    try:
        await Ninja(LeaveChannelRequest("@Ninja_Userbot"))
    except BaseException:
        pass
    try:
        await Ninja(LeaveChannelRequest("@Official_NinjaBot"))
    except BaseException:
        pass


spam = os.environ.get("SPAM", None) or "OFF"


async def scammer(username):
    i = 0
    xx = 0
    async for x in Ninja.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await Ninja.edit_permissions(x.id, username, view_messages=False)
                i += 1
            except:
                xx += 1
    print(f"OP {i-xx}")


async def spams():
    if spam == "ON":
        import glob

        path = "userbot/plugins/Spam/*.py"
        files = glob.glob(path)
        for name in files:
            with open(name) as f:
                path1 = Path(f.name)
                shortname = path1.stem
                start_spam(shortname.replace(".py", ""))
    else:
        print("⚠️Spam Not Loading⚠️")


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    type = False
    if BOTLOG:
        try:
            entity = await Ninja.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID cannot be found. Make sure it's correct."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID is unsupported. Make sure it's correct."
            )
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "Don't delete this group or change to group(If you change group all your previous snips, welcome will be lost.)"
        _, groupid = await create_supergroup(
            "NinjaBot Log Group", Ninja, Config.BOT_USERNAME, descript
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print(
            "Private Group for PRIVATE_GROUP_BOT_API_ID is created successfully and added to vars."
        )
        type = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await Ninja.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID cannot be found. Make sure it's correct.")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID is unsupported. Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PM_LOGGER_GROUP_ID.\n"
                + str(e)
            )
    if type:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
