from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from Pyrochiy.helpers.basic import edit_or_reply
from Pyrochiy.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


@Client.on_message(filters.command(["alquran", "quran"], cmd) & filters.me)
async def alquran_cmd(client: Client, message: Message):
    ram = await edit_or_reply(message, "`Tunggu Sebentar...`")
    await gather(
        ram.delete(),
        client.send_voice(
            message.chat.id,
            choice(
                [
                    alquran.voice.file_id
                    async for alquran in client.search_messages(
                        "Alquran_voicee", filter=enums.MessagesFilter.VOICE_NOTE
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )

@Client.on_message(filters.command(["sholawat", "slwt"], cmd) & filters.me)
async def sholawat_cmd(client: Client, message: Message):
    ram = await edit_or_reply(message, "`Tunggu Sebentar...`")
    await gather(
        ram.delete(),
        client.send_audio(
            message.chat.id,
            choice(
                [
                    sholawat.audio.file_id
                    async for sholawat in client.search_messages(
                        "sholawatmajelis", filter=enums.MessagesFilter.AUDIO
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )


add_command_help(
    "islamic",
    [
        [
            f"alquran atau {cmd}quran",
            "Untuk Mengirim Voice Not Alquran secara random.",
        ],
        [
            f"sholawat atau {cmd}slwt",
            "Untuk Mengirim Audio Sholawat Secara Random.",
        ],
    ],
)
