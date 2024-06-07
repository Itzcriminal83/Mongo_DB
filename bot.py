import re
import os
import random
import pymongo
import urllib

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Client(
    name="MongoBot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"],
    in_memory=True,
)


start_key = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/CRiMinAl_B0Y")
        ]
    ]
)


start_pics = [
    "https://te.legra.ph/file/be886890e66873984048f.jpg",
    "https://te.legra.ph/file/963fd1b8a5dbf20961e14.jpg",
    "https://te.legra.ph/file/ca11c6cfeb08c92f979a2.jpg",
    "https://te.legra.ph/file/6dc1bf48936cda7fa9371.jpg",
    "https://te.legra.ph/file/3c11427d0ed3719351da6.jpg",
    "https://te.legra.ph/file/78c22cf0faa8094ead29c.jpg",
    "https://te.legra.ph/file/4352eb1387b752dedb491.jpg",
]

START_TXT = """
**ʜɪɪ {}**, `ɪ ᴀᴍ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ᴄʜᴇᴄᴋᴇʀ ʙᴏᴛ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ɪ ᴡɪʟʟ ᴛᴇʟʟ ʏᴏᴜʀ ᴜʀʟ ʜᴀᴠɪɴɢ ᴀɴʏ ɪssᴜᴇs ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴏʀ ɴᴏᴛ.`
"""

@bot.on_message(filters.command("start"))
async def _start(_, msg: Message):
    chat_id = msg.chat.id  # Get the chat ID from the message object
    await bot.send_photo(
        chat_id=chat_id,  # Pass the chat ID as an argument
        photo=random.choice(start_pics),
        caption=START_TXT.format(msg.chat.first_name),  # Personalize the message
        has_spoiler=True,
        protect_content=True,
        reply_markup=start_key,
    )


@bot.on_message(filters.private & filters.text & ~filters.command(["start", "check"]))
async def _private_filter(_, msg: Message):
    url = msg.text
    await check_url(msg, url)
    await msg.delete()  # For Security


@bot.on_message(filters.command("check"))
async def _check(_, msg: Message):
    if len(msg.command) > 1:
        url = msg.command[1]
    else:
        return await msg.reply("`ᴜʀʟ ɴᴏᴛ ғᴏᴜɴᴅ!`")
    await check_url(msg, url) 
    try:
        await msg.delete()  # Will work also in group so Pass chat admin Exception.
    except:
        await msg.reply("`ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴛʜɪs ᴜʀʟ ᴍʏsᴇʟғ, ᴀɴʏ ᴀᴅᴍɪɴ ᴅᴇʟᴇᴛᴇ ᴛʜɪs ғᴏʀ sᴇᴄᴜʀɪᴛʏ.")


async def check_url(msg: Message, url: str):
    PATTERN = r"^mongodb((?:\+srv))?:\/\/(.*):(.*)@[a-z0-9]+\.(.*)\.mongodb\.net\/(.*)\?retryWrites\=true&w\=majority"
    s_r = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    match = re.match(PATTERN, url)
    if not match:   
        return await msg.reply(f"**ɪɴᴠᴀʟɪᴅ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ**: `{url}`")
    username, password, key, dbname = match.group(2), match.group(3), match.group(4), match.group(5)
    if s_r.search(username) or s_r.search(password):
        return await msg.reply(f"**ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ**: `{username}` and `{password}` must be escaped.")
    try: 
        pymongo.MongoClient(url)
    except Exception as e:
        return await msg.reply(f"**ᴇʀʀᴏʀ**: `{e}`")
    await msg.reply("`ᴛʜɪs ᴜʀʟ ɪs ᴇʀʀᴏʀ ғʀᴇᴇ. ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ.`")


if __name__ == "__main__":
    bot.run()
