from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, ADMINS, FORCE_SUB_CHANNELS, START_PIC, FORCE_PIC, SESSION_NAME, FORCE_MSG, START_MSG, CHANNEL_ID
from database import (
    add_user, is_banned, ban_user, unban_user,
    add_admin, remove_admin, is_admin, get_stats,
    add_file, search_files
)
from pyrogram.enums import ChatType

bot = Client(f"SESSION_NAME", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def is_forced(user):
    for ch in FORCE_SUB_CHANNELS.split(","):
        try:
            member = await bot.get_chat_member(ch.strip(), user)
            if member.status not in ("member", "administrator", "creator"):
                return True
        except:
            return True
    return False

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id):
        return await message.reply("**ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ...**")

    if await is_forced(message.from_user.id):
        buttons = [
            [InlineKeyboardButton(f"Jᴏɪɴ {ch.strip('@')}", url=f"https://t.me/{ch.strip()}")]
            for ch in FORCE_SUB_CHANNELS.split(",")
        ]
        return await message.reply_photo(
            FORCE_PIC,
            caption=FORCE_MSG,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    await message.reply_photo(START_PIC, caption=START_MSG)

@bot.on_message(filters.private & filters.command("stats"))
async def stats(client, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("**Yᴏᴜ ᴀʀᴇɴ'ᴛ ᴀɴ ᴀᴅᴍɪɴ.**")
    stats = get_stats()
    await message.reply(
        f"**Fɪʟᴇs: {stats['files']}\nUsᴇʀs: {stats['users']}\nAᴅᴍɪɴs: {stats['admins']}**"
    )

@bot.on_message(filters.command("addadmin"))
async def add_admin_cmd(client, message: Message):
    if not await is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        add_admin(user_id)
        await message.reply(f"**Aᴅᴅᴇᴅ {user_id} ᴀs ᴀᴅᴍɪɴ.**")
    except:
        await message.reply("**Usᴀɢᴇ: /addadmin <user_id>**")

@bot.on_message(filters.command("deladmin"))
async def del_admin_cmd(client, message: Message):
    if not await is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        remove_admin(user_id)
        await message.reply(f"**Rᴇᴍᴏᴠᴇᴅ {user_id} ғʀᴏᴍ ᴀᴅᴍɪɴ.**")
    except:
        await message.reply("**Usᴀɢᴇ: /deladmin <user_id>**")

@bot.on_message(filters.command("ban"))
async def ban_cmd(client, message: Message):
    if not await is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        await ban_user(user_id)
        await message.reply(f"**Bᴀɴɴᴇᴅ {user_id}**")
    except:
        await message.reply("**Usᴀɢᴇ: /ban <user_id>")

@bot.on_message(filters.command("unban"))
async def unban_cmd(client, message: Message):
    if not await is_admin(message.from_user.id): return
    try:
        user_id = int(message.command[1])
        await unban_user(user_id)
        await message.reply(f"**Uɴʙᴀɴɴᴇᴅ {user_id}**")
    except:
        await message.reply("**Usᴀɢᴇ: /unban <user_id>**")

@bot.on_message(filters.document & filters.private)
async def index_file(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id):
        return
    if await is_forced(message.from_user.id):
        return
    file_name = message.document.file_name
    file_size = message.document.file_size
    message_id = message.id
    await add_file(file_name, message_id, file_size)
    await message.reply("**Fɪʟᴇ Iɴᴅᴇxᴇᴅ.**")

@bot.on_message(filters.channel & filters.document)
async def index_channel_file(client, message: Message):
    file_name = message.document.file_name
    file_size = message.document.file_size
    message_id = message.id
    await add_file(file_name, message_id, file_size)

@bot.on_message(filters.private & filters.command("search_all"))
async def search_all_files(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id): return
    if await is_forced(message.from_user.id): return
    query = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    if not query:
        return await message.reply("**Usᴀɢᴇ: /search_all <query>**")
    results = search_files(query)
    if not results:
        return await message.reply("**Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")
    reply_text = "\n".join([
        f"**📄 [{r['file_name']}](https://t.me/{CHANNEL_ID}/{r['message_id']}) - {r['file_size']//1024} KB**"
        for r in results
    ])
    await message.reply(reply_text, disable_web_page_preview=True)

@bot.on_message(filters.private & filters.text & ~filters.command(["start", "stats", "addadmin", "deladmin", "ban", "unban", "search_all"]))
async def search_index(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id): return
    if await is_forced(message.from_user.id): return
    query = message.text.strip()
    results = list(search_files(query))
    if not results:
        return await message.reply("**Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")
    buttons = [
        [InlineKeyboardButton(text=f"{r['file_name'][:60]}", url=f"https://t.me/{CHANNEL_ID}/{r['message_id']}")]
        for r in results
    ]
    await message.reply(f"**Rᴇsᴜʟᴛs ғᴏʀ: {query}**", reply_markup=InlineKeyboardMarkup(buttons))

bot.run()

@bot.on_message(filters.document & filters.private)
async def index_file(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id): return
    if await is_forced(message.from_user.id): return
    file_name = message.document.file_name
    file_size = message.document.file_size
    message_id = message.id
    await add_file(file_name, message_id, file_size)
    await message.reply("**Fɪʟᴇ Iɴᴅᴇxᴇᴅ.**")

@bot.on_message(filters.private & filters.text & ~filters.command(["start", "stats", "addadmin", "deladmin", "ban", "unban"]))
async def search_index(client, message: Message):
    await add_user(message.from_user.id)
    if await is_banned(message.from_user.id): return
    if await is_forced(message.from_user.id): return
    query = message.text.strip()
    results = search_files(query)
    reply_text = "\n".join([
    f"📄 [{r['file_name']}]("
    f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}/{r['message_id']}) "
    f"- {r['file_size']//1024} KB"
    for r in results
])
    await message.reply(reply_text if reply_text else "**Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")

@bot.on_message(filters.channel & filters.document)
async def index_channel_file(client, message: Message):
    file_name = message.document.file_name
    file_size = message.document.file_size
    message_id = message.id
    await add_file(file_name, message_id, file_size)

bot.run()
