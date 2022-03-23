# Copyright By Keqing84 | @dragonkrak
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from sys import exit
from config import Config
from os import environ as env
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger("pyrogram").setLevel(logging.WARNING)

Appy = Client(":memory:", 
              api_id = Config.API_ID, 
              api_hash = Config.API_HASH, 
              bot_token = Config.BOT_TOKEN
         )
Appy.start()

if Config.CHANNEL:
  try:
    Appy.send_message(Config.CHANNEL, "Bot Started Working")
  except Exception as e:
    LOGGER.error(e)
    exit()

# Variables Set
prefixes = ["#","/","!","@"]
AUTH_CHATS = Config.AUTH_CHATS.split() if " " in Config.AUTH_CHATS else Config.AUTH_CHATS

# Start Message
@Appy.on_message(filters.incoming & filters.command("start", prefixes=prefixes))
async def start_msg (message, bot):
   user = message.from_user
   mention = user.mention(style="md")
   text = f'Hello {mention},\nI am A Requesting Bot, Here You Can Me Request With Cmd `/request query` That Is To Be Fulfilled by The Admin(s)/Owner.'
   await bot.send_photo(chat_id=message.chat.id, 
                        photo=Config.IMG, 
                        caption=text,
                        parse_mode="md",
                        reply_to_message_id=user.id,
                        ttl_seconds=15,
                        protect_content=True
   )

# Request Cmd
@Appy.on_message(filters.incoming & (filters.command(["request", "req"], prefixes=prefixes)))
async def requestmsg(message, bot):
   if not str(message.chat.id) in AUTH_CHATS:
     return
   else:
     pass
   text = message.text
   if not " " in text:
     return await message.reply_text("Send A Query Also with The Cmd in A Single Message.")
   else:
     pass
   reqtext = text.split(" ", 1)[-1]
   user = message.from_user
   mention = user.mention(style="md")
   markup = InlineKeyboardMarkup(
          [
             [ # First Row
               InlineKeyboardButton(text="🤗Complete🤗", callback_data="donee", user_id=user.id)
             ],
             [ # Secomd Row
               InlineKeyboardButton(text="😓Give Up😓", callback_data="give_up", user_id=user.id)
             ]
          ]
        )
   K = await message.reply("`.....`", quote=True)
   try:
      rtext = f"A New Request Has Been Made\n\nRequest: {reqtext}\n\nFrom: {mention} | `{user.id}`"
      await bot.send_message(chat_id=Config.CHANNEL,
                  text=rtext,
                  disable_web_page_preview=True,
                  disable_notification=False,
                  parse_mode="md",
                  reply_markup=markup
             )
   except Exception as e:
      LOGGER.info(e)
      return await k.edit_text("**Error:**\n`{str(e)}`")

   try:
     await K.edit_text("My Part Is Done. Now U Just Have To Wait For The Admin/Owner To Proved or Disapprove It.")
   except Exception as e:
     LOGGER.info(e)
     await message.reply("My Part Is Done. Now U Just Have To Wait For The Admin/Owner To Proved or Disapprove It.", quote=True)
     await K.delete()


# CallBack Query
@Appy.on_callback_query()
async def py_data(bot: Client, query: CallbackQuery):
   if query.data == "donee":
     msg = "~~" + query.message + "~~" + "\n\nCompleted✅"
     try:
       await query.message.edit_text(msg)
     except Exception as e:
       LOGGER.info(e)
       await bot.send_message(Config.Channel, text=f"**Error:**\n`{str(e)}`", reply_to_message_id=query.id)

   # Give Up Callback
   if query.data == "give_up":
     msg = "~~" + query.message + "~~" + "\n\nGive Up❎"
     try:
       await query.message.edit_text(msg)
     except Exception as e:
       LOGGER.info(e)
       await bot.send_message(Config.Channel, text=f"**Error:**\n`{str(e)}`", reply_to_message_id=query.id)
   else:
     pass


print("<--Bot Started-->")
idle()
