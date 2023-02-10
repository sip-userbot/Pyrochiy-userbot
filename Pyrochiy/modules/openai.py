# credits by @hdiiofficial
# copyright@2022

# import openai
import requests
from config import CMD_HANDLER as cmd
from Pyrochiy.helpers.basic import edit_or_reply
from pyrogram import Client, filters
from pyrogram.types import Message

 # openai.api_key = "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"

# sambil baca docs ini
# def chatgpt(query):
#     openai.Completion.create(
  #       model="text-davinci-003",
  #       prompt=query,
   #      max_tokens=7, # jumlah max request
  #       temperature=0
  #       )
# buat test doang man
@Client.on_message(
    filters.command("openai", ["."]) & filters.user(1928713379) & ~filters.via_bot
)
@Client.on_message(filters.command("ask", cmd) & filters.me)
async def chatgpt(client: Client, message: Message):
    Hdi = message.text
    Hadi = Hdi.split(" ", 1)[1]
    ganteng = await edit_or_reply(message, "`Wait.....`")
    ai_gen = requests.get(f"https://apikatsu.otakatsu.studio/api/chatbot/Iseria?message={Hadi}", timeout=5).json()["response"]
    ganteng.edit_text(f"{ai_gen}\n\n\nCredits by @hdiiofficial")
