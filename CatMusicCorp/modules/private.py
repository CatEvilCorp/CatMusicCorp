
import logging
from time import time
from datetime import datetime
from CatMusicCorp.config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, SUPPORT_GROUP
from CatMusicCorp.helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from CatMusicCorp.helpers.decorators import sudo_users_only

logging.basicConfig(level=logging.INFO)


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>โจ **Welcome {message.from_user.first_name}** \n
๐ญ **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) ๐ฎ๐น๐น๐ผ๐ ๐๐ผ๐ ๐๐ผ ๐ฝ๐น๐ฎ๐ ๐บ๐๐๐ถ๐ฐ ๐ผ๐ป ๐ด๐ฟ๐ผ๐๐ฝ๐ ๐๐ต๐ฟ๐ผ๐๐ด๐ต ๐๐ต๐ฒ ๐ป๐ฒ๐ ๐ง๐ฒ๐น๐ฒ๐ด๐ฟ๐ฎ๐บ'๐ ๐๐ผ๐ถ๐ฐ๐ฒ ๐ฐ๐ต๐ฎ๐๐ !**

๐ก **๐๐ถ๐ป๐ฑ ๐ผ๐๐ ๐ฎ๐น๐น ๐๐ต๐ฒ ๐๐ผ๐'๐ ๐ฐ๐ผ๐บ๐บ๐ฎ๐ป๐ฑ๐ ๐ฎ๐ป๐ฑ ๐ต๐ผ๐ ๐๐ต๐ฒ๐ ๐๐ผ๐ฟ๐ธ ๐ฏ๐ ๐ฐ๐น๐ถ๐ฐ๐ธ๐ถ๐ป๐ด ๐ผ๐ป ๐๐ต๐ฒ ยป ๐ ๐๐ผ๐บ๐บ๐ฎ๐ป๐ฑ๐ ๐ฏ๐๐๐๐ผ๐ป !**

โ **๐๐ผ๐ฟ ๐ถ๐ป๐ณ๐ผ๐ฟ๐บ๐ฎ๐๐ถ๐ผ๐ป ๐ฎ๐ฏ๐ผ๐๐ ๐ฎ๐น๐น ๐ณ๐ฒ๐ฎ๐๐๐ฟ๐ฒ ๐ผ๐ณ ๐๐ต๐ถ๐ ๐ฏ๐ผ๐, ๐ท๐๐๐ ๐๐๐ฝ๐ฒ /help**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "โ Add me to your Group โ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "โ How to use Me", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         "๐ Commands", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "๐ Donate", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "๐ฅ Official Group", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton(
                        "๐ฃ Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "๐งช Source Code ๐งช", url="https://github.com/QueenArzoo/CatMusicCorp"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""โ **bot is running**\n<b>๐? **uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "โจ Group", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton(
                        "๐ฃ Channel", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>๐๐ป **Hello** {message.from_user.mention()}</b>

**Please press the button below to read the explanation and see the list of available commands !**

โก __Powered by {BOT_NAME} A.I""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="โ HOW TO USE ME", callback_data="cbguide"
                    )
                ]
            ]
        ),
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>๐ก Hello {message.from_user.mention} welcome to the help menu !</b>

**in this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

โก __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "๐ Basic Cmd", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "๐ Advanced Cmd", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "๐ Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "๐ Sudo Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "๐ Owner Cmd", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "๐ Fun Cmd", callback_data="cbfun"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "๐ `PONG!!`\n"
        f"โก๏ธ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "๐ค bot status:\n"
        f"โข **uptime:** `{uptime}`\n"
        f"โข **start time:** `{START_TIME_ISO}`"
    )
