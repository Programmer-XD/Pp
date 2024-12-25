from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
import random
from . import user_collection, app, capsify
from Grabber import *

sudb = db.sudo
devb = db.dev
uploaderdb = db.uploader

@app.on_message(filters.command("start") & filters.private)
async def start_command_private(_, message):
    user_id = message.from_user.id
    user = await _.get_users(user_id)
    username = user.username
    first_name = user.first_name

    user_collection.update_one(
        {"id": user_id},
        {"$set": {"username": username, "first_name": first_name}},
        upsert=True
    )

    random_video = random.choice(PHOTO_URL)
    await _.send_video(
        chat_id=user_id,
        video=random_video,
        caption=capsify(f"👋 Hi, this is {BOT_USERNAME}, an anime-based games bot! Add me to your group to start your journey."),
        reply_markup=IKM([
            [IKB(capsify("Support"), url=f"https://t.me/{SUPPORT_CHAT}"),
             IKB(capsify("Updates"), url=f"https://t.me/{UPDATE_CHAT}")],
            [IKB(capsify("Add Me Baby 🐥"), url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [IKB(capsify("Help"), url=f"https://t.me/{SUPPORT_CHAT}"),
             IKB(capsify("Credits"), callback_data="show_credits")]
        ])
    )

@app.on_message(filters.command("start") & filters.group)
async def start_command_group(_, message):
    await message.reply_text(
        capsify("🚀 To start using me, please click the button below to initiate in DM."),
        reply_markup=IKM([
            [IKB(capsify("Start in DM"), url=f"https://t.me/{BOT_USERNAME}")]
        ])
    )


@app.on_callback_query(filters.regex("show_credits"))
async def show_credits(_, message_or_callback):
    if isinstance(message_or_callback, Client):
        message = message_or_callback
        await message.reply_text(
            text=capsify(
                "Bot Credits\n\n"
                "Users below are the developers, uploaders, etc... of this bot, you can personally contact em for issues, do not dm unnecessarily.\n\n"
                "Thank You ❗"
            ),
            reply_markup=IKM([
                [IKB(capsify("Developers"), callback_data="show_dev_names"),
                 IKB(capsify("Sudos"), callback_data="show_sudo_names")],
                [IKB(capsify("Uploads"), callback_data="show_uploader_names"),
                 IKB(capsify("Back"), callback_data="start_main_menu")]
            ])
        )
    else:
        callback_query = message_or_callback
        await callback_query.edit_message_text(
            text=capsify(
                "Bot Credits\n\n"
                "Users below are the developers, uploaders, etc... of this bot, you can personally contact em for issues, do not dm unnecessarily.\n\n"
                "Thank You ❗"
            ),
            reply_markup=IKM([
                [IKB(capsify("Developers"), callback_data="show_dev_names"),
                 IKB(capsify("Sudos"), callback_data="show_sudo_names")],
                [IKB(capsify("Uploads"), callback_data="show_uploader_names"),
                 IKB(capsify("Back"), callback_data="start_main_menu")]
            ])
        )



@app.on_callback_query(filters.regex("start_main_menu"))
async def start_main_menu(_, callback_query):
    user_id = callback_query.from_user.id
    user = await _.get_users(user_id)
    username = user.username
    first_name = user.first_name

    random_video = random.choice(PHOTO_URL)
    await callback_query.edit_message_text(
        text=capsify(f"👋 Hi, this is {BOT_USERNAME}, an anime-based games bot! Add me to your group to start your journey."),
        caption=random_video,
        reply_markup=IKM([
            [IKB(capsify("Support"), url=f"https://t.me/{SUPPORT_CHAT}"),
             IKB(capsify("Updates"), url=f"https://t.me/{UPDATE_CHAT}")],
            [IKB(capsify("Add Me Baby 🐥"), url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [IKB(capsify("Help"), url=f"https://t.me/{SUPPORT_CHAT}"),
             IKB(capsify("Credits"), callback_data="show_credits")]
        ])
    )

@app.on_message(filters.command("credits"))
async def credits_command(_, message):
    await message.reply_text(
        text=capsify(
            "Bot Credits\n\n"
            "Users below are the developers, uploaders, etc... of this bot, you can personally contact them for issues, do not DM unnecessarily.\n\n"
            "Thank You!"
        ),
        reply_markup=IKM([
            [IKB(capsify("Developers"), callback_data="show_dev_names"),
             IKB(capsify("Sudos"), callback_data="show_sudo_names")],
            [IKB(capsify("Uploads"), callback_data="show_uploader_names"),
             IKB(capsify("Back"), callback_data="start_main_menu")]
        ])
    )

@app.on_callback_query(filters.regex("show_dev_names"))
async def show_dev_names(_, callback_query):
    await callback_query.edit_message_text(
        text=capsify("Loading developer names..."),
        reply_markup=IKM([
            [IKB(capsify("Back"), callback_data="show_credits")]
        ])
    )

    dev_buttons = []
    async for user in devb.find():
        dev_id = user.get("user_id")
        if dev_id:
            try:
                user = await _.get_users(dev_id)
                name = user.first_name or "Unknown"
                dev_buttons.append(IKB(capsify(name), user_id=dev_id))
            except Exception:
                dev_buttons.append(IKB(capsify("Unknown"), user_id=dev_id))

    # Limit to 4 rows, or as needed
    rows = [dev_buttons[i:i+3] for i in range(0, min(len(dev_buttons), 12), 3)]
    await callback_query.edit_message_text(
        text=capsify("**Developers:**"),
        reply_markup=IKM(rows + [[IKB(capsify("Back"), callback_data="show_credits")]])
    )

@app.on_callback_query(filters.regex("show_sudo_names"))
async def show_sudo_names(_, callback_query):
    await callback_query.edit_message_text(
        text=capsify("Loading sudo names..."),
        reply_markup=IKM([
            [IKB(capsify("Back"), callback_data="show_credits")]
        ])
    )

    sudo_buttons = []
    async for user in sudb.find():
        sudo_id = user.get("user_id")
        if sudo_id:
            try:
                user = await _.get_users(sudo_id)
                name = user.first_name or "Unknown"
                sudo_buttons.append(IKB(capsify(name), user_id=sudo_id))
            except Exception:
                sudo_buttons.append(IKB(capsify("Unknown"), user_id=sudo_id))

    rows = [sudo_buttons[i:i+3] for i in range(0, min(len(sudo_buttons), 12), 3)]
    await callback_query.edit_message_text(
        text=capsify("**Sudos:**"),
        reply_markup=IKM(rows + [[IKB(capsify("Back"), callback_data="show_credits")]])
    )

@app.on_callback_query(filters.regex("show_uploader_names"))
async def show_uploader_names(_, callback_query):
    await callback_query.edit_message_text(
        text=capsify("Loading uploader names..."),
        reply_markup=IKM([
            [IKB(capsify("Back"), callback_data="show_credits")]
        ])
    )

    uploader_buttons = []
    async for user in uploaderdb.find():
        uploader_id = user.get("user_id")
        if uploader_id:
            try:
                user = await _.get_users(uploader_id)
                name = user.first_name or "Unknown"
                uploader_buttons.append(IKB(capsify(name), user_id=uploader_id))
            except Exception:
                uploader_buttons.append(IKB(capsify("Unknown"), user_id=uploader_id))

    rows = [uploader_buttons[i:i+3] for i in range(0, min(len(uploader_buttons), 12), 3)]
    await callback_query.edit_message_text(
        text=capsify("**Uploaders:**"),
        reply_markup=IKM(rows + [[IKB(capsify("Back"), callback_data="show_credits")]])
    )