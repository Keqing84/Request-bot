# Copyright By Keqing84 | @dragonkrak

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from pyrogram.errors import FloodWait
from config import Config
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client(
         ":memory:", 
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
@app.on_message(filters.private & filters.command("start", prefixes=prefixes))
async def start_msg(message: Message, bot: Client):
   user = message.from_user
   mention = user.mention(style="md")
   text = f'Hello {mention},\nI am A Requesting Bot, Here You Can Me Request With Cmd `/request query` That Is To Be Fulfilled by The Admin(s)/Owner.'
   await bot.send_photo(chat_id=message.chat.id, 
                        photo=Config.IMG, 
                        caption=text,
                        parse_mode="md",
                        protect_content=True
   )

# Request Cmd
@app.on_message(~filters.edited & filters.command(["request", "req"], prefixes=prefixes))
async def request_msg(message: Message, bot: Client):
   id = message.chat.id
   if str(id) in AUTH_CHATS:
     pass
   else:
     return
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
@app.on_callback_query()
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


LOGGER.info("<--Bot Started-->")
Appy.run()
