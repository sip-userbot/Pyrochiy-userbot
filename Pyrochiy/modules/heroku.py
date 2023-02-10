
import asyncio
import math
import dotenv
import heroku3
import requests
import urllib3
from Pyrochiy.utils.misc import *
from pyrogram import Client, filters

from config import HEROKU_API_KEY, HEROKU_APP_NAME
from config import CMD_HNDLR as cmds
from Pyrochiy import SUDO_USER, Client


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


@Client.on_message(filters.command("logs", cmds) & filters.user(SUDO_USER))
async def log_(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
    else:
        return await message.reply_text("Only for Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    data = happ.get_log()
    if len(data) > 1024:
        link = await paste_queue(data)
        url = link + "/index.txt"
        return await message.reply_text(
            f"Here is the Log of Your App[{HEROKU_APP_NAME}]\n\n[Click Here to checkout Logs]({url})"
        )
    else:
        return await message.reply_text(data)


@Client.on_message(filters.command("get_var", cmds) & filters.user(SUDO_USER))
async def varget_(client, message):
    usage = "**Usage:**\n/get_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            return await message.reply_text(
                f"**Heroku Config:**\n\n**{check_var}:** `{heroku_config[check_var]}`"
            )
        else:
            return await message.reply_text("No such Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.get_key(path, check_var)
        if not output:
            return await message.reply_text("No such Var")
        else:
            return await message.reply_text(
                f".env:\n\n**{check_var}:** `{str(output)}`"
            )


@Client.on_message(filters.command("del_var", cmds) & filters.user(SUDO_USER))
async def vardel_(client, message):
    usage = "**Usage:**\n/del_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            await message.reply_text(
                f"**Heroku Var Deletion:**\n\n`{check_var}` has been deleted successfully."
            )
            del heroku_config[check_var]
        else:
            return await message.reply_text(f"No such Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.reply_text("No such Var")
        else:
            return await message.reply_text(
                f".env Var Deletion:\n\n`{check_var}` has been deleted successfully. To restart the bot touch /restart command."
            )


@Client.on_message(filters.command("set_var", cmds) & filters.user(SUDO_USER))
async def set_var(client, message):
    usage = "**Usage:**\n/set_var [Var Name] [Var Value]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.reply_text(
                f"**Heroku Var Updation:**\n\n`{to_set}` has been updated successfully. Bot will Restart Now."
            )
        else:
            await message.reply_text(
                f"Added New Var with name `{to_set}`. Bot will Restart Now."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.reply_text(
                f"**.env Var Updation:**\n\n`{to_set}`has been updated successfully. To restart the bot touch /restart command."
            )
        else:
            return await message.reply_text(
                f"**.env dəyişən əlavə edilməsi:**\n\n`{to_set}` has been added sucsessfully. To restart the bot touch /restart command."
            )


@Client.on_message(
    filters.command(["usage"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def usage_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
    else:
        return await message.reply_text("Only for Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
        )
    dyno = await message.reply_text("Checking Heroku Usage. Please Wait")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    day = math.floor(hours / 24)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
✥ **Informasi Dyno Heroku :**
╔════════════════════╗
 ➠ **Penggunaan Dyno** `{HEROKU_APP_NAME}` :
     •  `{AppHours}`**Jam**  `{AppMinutes}`**Menit |**  [`{AppPercentage}`**%**]
 ➠ **Sisa kuota dyno bulan ini** :
     •  `{hours}`**Jam**  `{minutes}`**Menit |**  [`{percentage}`**%**]
╚════════════════════╝
✥ **Sisa Dyno Heroku** `{day}` **Hari Lagi**"""
    return await dyno.edit(text)
