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
    api_id=int(os.environ["17097054"]),
    api_hash=os.environ["7d4ad6cc94b26157dacf1afe3b3e4b58"],
    bot_token=os.environ["6865147782:AAHR8MMwV0zs7Z_lKA-dKjD5LomUmPRWboM"],
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


@bot.on_message(filters.command("start"))
async def _start(_, msg: Message):
    await app.send_photo(
        chat_id=message.chat.id,
        photo=random.choice(start_pics),
        caption=f"нєу {message.from_user.first_name},\n ᴛʜɪs ɪs {app.mention},\n\nᴀ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ᴄʜᴇᴄᴋᴇʀ ʙᴏᴛ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴜʀʟ ɪ ᴡɪʟʟ ᴛᴇʟʟ ʏᴏᴜʀ ᴜʀʟ ʜᴀᴠɪɴɢ ᴀɴʏ ɪssᴜᴇs ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴏʀ ɴᴏᴛ.",
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
    try: 
        pymongo.MongoClient(url)
    except Exception as e:
        if "Username and password must be escaped" in str(e):
            if bool(match.group(1)):
                raw_url = "mongodb+srv://{}:{}@cluster0.{}.mongodb.net/{}?retryWrites=true&w=majority"
            else:
                raw_url = "mongodb://{}:{}@cluster0.{}.mongodb.net/{}?retryWrites=true&w=majority"
            username, password, key, dbname = match.group(2), match.group(3), match.group(4), match.group(5)
            if s_r.search(username):
                username = urllib.parse.quote_plus(username)
            if s_r.search(password):
                password = urllib.parse.quote_plus(password)
            if '<' or '>' in dbname:
                dbname = "Userge"
            new_url = raw_url.format(username, password, key, dbname)
            await msg.reply( 
                "`ʏᴏᴜʀ ᴜʀʟ ʜᴀᴠɪɴɢ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ.`\n\n"
                "`ɪ ǫᴜᴏᴛᴇᴅ ʏᴏᴜʀ ᴜsᴇʀɴᴀᴍᴇ ᴀɴᴅ ᴘᴀssᴡᴏʀᴅ ᴀɴᴅ ᴄʀᴇᴀᴛᴇᴅ ɴᴇᴡ DB_URI, "
                f"ᴜsᴇ ᴛʜɪs ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ.`\n\n`{new_url}`"
            )
    else:
        if ('<' or '>') in match.group(5):
            dbname = "Userge"
            new_url = url.replace(match.group(5), dbname)
            return await msg.reply(f"`you forgot to remove '<' and '>' signs.`\n\n**Use this URL:** `{new_url}`")
        await msg.reply("`ᴛʜɪs ᴜʀʟ ɪs ᴇʀʀᴏʀ ғʀᴇᴇ. ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴍᴏɴɢᴏᴅʙ.`")


if __name__ == "__main__":
    bot.run()
