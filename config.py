from dotenv import load_dotenv
from os import environ as env, path as ospath

if ospath.exists(".env"):
   load_dotenv()

class Config:
    API_ID = int(env.get('API_ID')) 
    API_HASH = env.get('API_HASH')
    BOT_TOKEN = env.get('BOT_TOKEN')
    CHANNEL = int(env.get('CHANNEL'))
    AUTH_CHATS = env.get('AUTH_CHATS') # Add All The Auth Chats in a single string with space to separate 
    ADMIN = env.get('ADMIN') # Add All in single String with space to separate 
    IMG = env.get('IMG', "https://te.legra.ph/file/013eb4b121d22240d777c.jpg")

# Ex:
# AUTH_CHATS = "-10072617164 -10097976546"
# ADMIN = "46786794 94679675"
