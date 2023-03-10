import requests
from pyrogram import Client as Bot

from CatMusicCorp.config import API_HASH
from CatMusicCorp.config import API_ID
from CatMusicCorp.config import BG_IMAGE
from CatMusicCorp.config import BOT_TOKEN
from CatMusicCorp.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="CatMusicCorp.modules"),
)

bot.start()
run()
