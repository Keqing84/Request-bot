from os import environ as env

class Config:
    API_ID = env.get('API_ID')
    API_HASH = env.get('API_HASH')
    BOT_TOKEN = env.get('BOT_TOKEN')
    CHANNEL = env.get('CHANNEL')
    AUTH_CHATS = env.get('AUTH_CHATS')
