# (C) @Ansaku

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = os.environ["REMOVEBG_API"]
IMG_PATH = "./DOWNLOADS"

Bot = Client(
    "Penghapus Background",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
Hai {}, Saya adalah bot penghapus latar belakang foto. Kirimi saya foto, saya akan mengirim foto tanpa latar belakang.

Dibuat oleh @AnkiSatya
"""
HELP_TEXT = """
- Kirimkan saya foto
- Saya akan mengunduhnya
- Dan saya akan mengirim foto tanpa latar belakang

Dibuat oleh @AnkiSatya
"""
ABOUT_TEXT = """
- **Bot :** `Penghapus Background`
- **Pembuat :** [𝔸𝕟𝕜𝕚 𝕊𝕒𝕥𝕪𝕒](https://t.me/AnkiSatya)
- **Channel :** [𝕬𝖓𝖘𝖆𝖐𝖚 𝕭𝖔𝖙 𝕮𝖍𝖆𝖓𝖓𝖊𝖑](https://t.me/ansakubotchannel)
- **Sumber :** [Github](https://github.com/Ansaku/Penghapus-Background)
- **Donasi :** [Saweria](https://saweria.co/ansaku)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://t.me/ansakubotchannel'),
        InlineKeyboardButton('Masukan', url='https://t.me/AnkiSatya')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ERROR_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Join Updates Channel', url='https://t.me/ansakubotchannel')
        ]]
    )

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & (filters.photo | filters.document))
async def remove_background(bot, update):
    if not API:
        await update.reply_text(
            text="Error :- Remove BG Api error",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("mengetik")
    message = await update.reply_text(
        text="Menganalisa",
        quote=True,
        disable_web_page_preview=True
    )
    if (update and update.media and (update.photo or (update.document and "image" in update.document.mime_type))):
        file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "image.jpg"
        new_file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "no_bg.png"
        await update.download(file_name)
        await message.edit_text(
            text="Foto berhasil diunduh. Sekarang menghapus latar belakang.",
            disable_web_page_preview=True
        )
        try:
            new_image = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": open(file_name, "rb")},
                data={"size": "auto"},
                headers={"X-Api-Key": API}
            )
            if new_image.status_code == 200:
                with open(f"{new_file_name}", "wb") as image:
                    image.write(new_image.content)
            else:
                await update.reply_text(
                    text="API error.",
                    quote=True,
                    reply_markup=ERROR_BUTTONS
                )
                return
            await update.reply_chat_action("upload_photo")
            await update.reply_document(
                document=new_file_name,
                quote=True
            )
            await message.delete()
            try:
                os.remove(file_name)
            except:
                pass
        except Exception as error:
            print(error)
            await message.edit_text(
                text="Ada yang salah! Mungkin API limits.",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
    else:
        await message.edit_text(
            text="Media tidak didukung",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )

Bot.run()
