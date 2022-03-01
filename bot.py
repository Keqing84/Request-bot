from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from config import Config
from os import environ as env

Appy = Client("Request Bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

prefixes = ["#","/","!","@"]
photo = env.get("IMG") if len(env.get("IMG")) != 0 else "https://imgwhale.xyz/16mc8wom21l07utmtw"
AUTH_CHATS = Config.AUTH_CHATS.split() if " " in Config.AUTH_CHATS else Config.AUTH_CHATS

# Start Message
@Appy.on_message(filters.incoming & filters.command("start", prefixes=prefixes))
async def start_msg (message, bot):
   user = message.from_user
   mention = user.mention()
   text = f'Hello {mention},\nI am A Requesting Bot, Here You Can Me Request With Cmd `/request query` That Is To Be Fulfilled by The Admins/Owner.'
   await bot.send_photo(chat_id=message.chat.id, 
                        photo=photo, 
                        caption=text,
                        reply_to_message_id=user.id,
                        ttl_seconds=15,
                        protect_content=True
   )

# Request Cmd
@Appy.on_message(filters.incoming & filters.command("start", prefixes=prefixes))
async def startmsg (message, bot):
   if not str(message.chat.id) in AUTH_CHATS:
     return
   else:
     pass
   text = message.text
   if not " " in text:
     return await message.reply_text("Send A Query Also with The Cmd in A Single Message.")
   else:
     pass
   text = text.split(" ", 1)[-1]
   user = message.from_user
   mention = user.mention()
   markup = InlineKeyboardMarkup(
          [
             [ # First Row
               InlineKeyboardButton(text="🤗Complete🤗", callback_data="donee", user_id=user.id)
             ]
             [ # Secomd Row
               InlineKeyboardButton(text="😓Give Up😓", callback_data="give_up", user_id=user.id)
             ]
          ]
        )
   K = await message.reply("`.....`", quote=True)
   try:
       await bot.send_message(chat_id=Config.CHANNEL,
                  text=f"",
                  disable_web_page_preview=True,
                  disable_notification=False,
                  parse_mode="md",
                  reply_markup=markup
             )
   except Exception as e:
      return await k.edit_text("**Error:**\n`{e}`)
   await K.edit_text("My Part Is Done. Now U Just Have To Wait For The Admin/Owner To Proved or Disapprove It.")



