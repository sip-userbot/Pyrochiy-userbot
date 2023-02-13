import os
import sys
from pyrogram import Client



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Pyrochiy"])

async def join(client):
    try:
        await client.join_chat("ShicyyXCode")
        await client.join_chat("ShicyxC0d")
        await client.join_chat("StoryyCard")
    except BaseException:
        pass
