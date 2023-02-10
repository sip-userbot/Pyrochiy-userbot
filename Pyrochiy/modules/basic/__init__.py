import os
import sys
from pyrogram import Client



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Pyrochiy"])

async def join(client):
    try:
        await client.join_chat("shicyyC0d")
        await client.join_chat("ShicyyC0de")
        await client.join_chat("storyCarrd")
    except BaseException:
        pass
