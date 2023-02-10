import importlib
from pyrogram import idle
from uvloop import install


from Pyrochiy.modules import ALL_MODULES
from Pyrochiy import BOTLOG_CHATID, LOGGER, LOOP, aiosession, app, bots, ids
from Pyrochiy.modules.basic import join

BOT_VER = "0.1.0"
CMD_HANDLER = ["." "," "?" "!"]
MSG_ON = """
🔥 **Pyrochiy Telah Hidup** 🔥
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
❍▹ **Userbot Version -** `{}`
❍▹ **Ketik** `{}alive` **untuk Mengecek Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""


async def main():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("Pyrochiy.modules" + all_module)
        print(f"Successfully Imported {all_module} ")
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            try:
                await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER))
            except BaseException:
                pass
            print(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Pyrochiy").info("Pyrochiy Telah Hidup")
    install()
    LOOP.run_until_complete(main())
