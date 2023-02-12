# Copyright By Keqing84 | @dragonkrak

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import FloodWait
from config import Config
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(message)s')

logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client(
         "Req Bot", 
         api_id = Config.API_ID, 
         api_hash = Config.API_HASH, 
         bot_token = Config.BOT_TOKEN
         )

# Variables Set
prefixes = ["#","/","!","@"]
AUTH_CHATS = set()
if " " in Config.AUTH_CHATS:
    achats = Config.AUTH_CHATS.split(" ")
    for chats in achats:
        AUTH_CHATS.add(int(chats))
else:
    AUTH_CHATS.add(int(Config.AUTH_CHATS))

# Start Message
@app.on_message(~filters.edited & filters.command("start", prefixes=prefixes))
async def start_msg(_, msg: Message):
   mention = msg.from_user.mention(style="md")
   text = f'Hello {mention},\n**I am A Requesting Bot, Here You Can Me Request With Cmd `/request query` That Is To Be Fulfilled by The Admin(s)/Owner.**'
   await msg.reply_photo(
             Config.IMG, 
             caption=text,
             parse_mode="md",
             quote=True
     )

# Request Cmd
@app.on_message(~filters.edited & filters.command("request", prefixes=prefixes))
async def request_msg(_, msg: Message):
   id = msg.chat.id
   if not id in AUTH_CHATS:
     return
   text = msg.text
   if not " " in text:
     return await msg.reply_text("Send A Query Also with The Cmd in A Single Message.", quote=True)
   else:
     pass
   reqtext = text.split(" ", 1)[-1]
   mention = msg.from_user.mention(style="md")
   markup = InlineKeyboardMarkup(
          [
             [ # First Row
               InlineKeyboardButton(text="🤗Complete🤗", callback_data="donee", user_id=msg.from_user.id)
             ],
             [ # Secomd Row
               InlineKeyboardButton(text="😓Give Up😓", callback_data="give_up", user_id=msg.from_user.id)
             ]
          ]
        )
   K = await msg.reply("`.....`", quote=True)
   try:
      rtext = f"**New Request**\n\nRequest: {reqtext}\n\nFrom: {mention} | `{msg.from_user.id}`"
      await app.send_message(chat_id=Config.CHANNEL,
                  text=rtext,
                  disable_web_page_preview=True,
                  disable_notification=False,
                  parse_mode="md",
                  reply_markup=markup
             )
   except Exception as e:
      LOGGER.info(e)
      return await K.edit_text("**Error:**\n\n`{str(e)}`")

   try:
     await K.edit_text("**My Part Is Done. Now U Just Have To Wait For The Admin/Owner To Proved or Disapprove It.**")
   except Exception as e:
     LOGGER.info(e)
     await msg.reply("**My Part Is Done. Now U Just Have To Wait For The Admin/Owner To Proved or Disapprove It.**")
     await K.delete()


# CallBack Query
@app.on_callback_query()
async def py_data(_, query: CallbackQuery):
   if query.data == "donee":
     msg = "~~" + query.message.text + "~~" + "\n\nCompleted✅"
     try:
       await query.message.edit_text(msg)
     except Exception as e:
       LOGGER.info(e)
       await app.send_message(Config.Channel, text=f"**Error:**\n`{str(e)}`", reply_to_message_id=query.id)

   # Give Up Callback
   if query.data == "give_up":
     msg = "~~" + query.message.text + "~~" + "\n\nGive Up❎"
     try:
       await query.message.edit_text(msg)
     except Exception as e:
       LOGGER.info(e)
       await app.send_message(Config.Channel, text=f"**Error:**\n`{str(e)}`", reply_to_message_id=query.id)
   else:
     pass


LOGGER.info("<--Bot Started-->")
app.run()
