import asyncio
from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime, timedelta



class TBot:
    def __init__(self, app: Client):
        self.app = app
        


    async def get_messages(self, chat_id: int, messages_age: int):
        messages = []
        
        try:
            offset_date = datetime.now()
            dl_date = (offset_date - timedelta(days = messages_age)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)

            async for message in self.app.get_chat_history(chat_id, offset_date = offset_date):
                messages.append(message)

                if message.date.timestamp() < dl_date.timestamp():
                    break

            await asyncio.sleep(1)

        except Exception as e:
            print(e)
            pass

        return messages
    


    async def get_data(self, messages: list[Message]):
        data = []
        
        try:
            for message in messages:
                id = message.id
                date = message.date
                text = message.caption or message.text if message.caption or message.text else 'Без текста'
                link = message.link

                chat = message.chat
                chat_id = chat.id if chat else 'Не указано'
                chat_title = chat.title if chat else 'Не указано'
                chat_username = chat.username if chat else 'Не указано'
                chat_link = f"https://t.me/{chat_username}" if chat_username != 'Не указано' else 'Не указан chat_username'

                data.append({
                    "id" : id,
                    "date" : date,
                    "text" : text,
                    "link" : link,
                    "chat_id" : chat_id,
                    "chat_title" : chat_title,
                    "chat_username" : chat_username,
                    "chat_link" : chat_link
                })

        except:
            pass

        return data