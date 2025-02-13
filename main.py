import os
import asyncio
from pyrogram import Client
from dotenv import load_dotenv
from pyrogram.types import Message

from py.saver import Saver
from py.telegram import TBot

PHONE = os.getenv('PHONE')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SAVE_FOLDER = os.getenv('SAVE_FOLDER')
MESSAGES_AGE = int(os.getenv('MESSAGES_AGE')) if int(os.getenv('MESSAGES_AGE')) >= 0 else 0
MONITORED_CHATS = [int(item.strip()) for item in os.getenv('MONITORED_CHATS').split(',') if item]
MONITORED_CHATS = list(dict.fromkeys(MONITORED_CHATS))


try:
    app = Client("pyrogram_data", api_id = API_ID, api_hash = API_HASH, phone_number = PHONE)
except:
    input("[ERROR] Не удалось подключиться к серверам Telegram")
    exit()



async def show_settings():
    print()
    print(f"----------------- НАСТРОЙКИ ------------------")
    print(f"   * Телефон:                {'ПОЛУЧЕН' if PHONE else 'ПУСТ'}")
    print(f"   * API ID:                 {'ПОЛУЧЕН' if API_ID else 'ПУСТ'}")
    print(f"   * API HASH:               {'ПОЛУЧЕН' if API_HASH else 'ПУСТ'}")
    print(f"   * Папка сохранений:       /{SAVE_FOLDER}")
    print(f"   * Возраст сообщений:      до {MESSAGES_AGE} дней")
    print(f"   * Отслеживаемые каналы:   {len(MONITORED_CHATS)} шт.")
    print()



async def collect_messages():
    saver = Saver()
    tbot = TBot(app)
    
    print("[WORK] Обработка каналов:")
    
    total_data = []

    for index, chat_id in enumerate(MONITORED_CHATS):
        index = f"{index + 1}/{len(MONITORED_CHATS)}"
  
        messages: list[Message] = await tbot.get_messages(chat_id, MESSAGES_AGE)

        if not messages:
            print(f"   [{index}] Не удалось получить сообщения от канала '{chat_id}'.")
            continue
        
        data = await tbot.get_data(messages)

        if not data:
            print(f"   [{index}] Не удалось извлечь информацию из сообщений от канала '{chat_id}'.")
            continue
        
        total_data.extend(data)

        filename = saver.get_valid_filename(f"messages{chat_id}.xlsx")
        status = f'Сохранено ({len(data)} шт.)' if saver.save_as_xlsx(SAVE_FOLDER, filename, data) else 'Не удалось сохранить'

        print(f"   [{index}] Статус канала {chat_id}: {status}")

    print()
    


    status = f'Сохранено ({len(total_data)} шт.)' if saver.save_as_xlsx(SAVE_FOLDER, "all-messages.xlsx", total_data) else 'Не удалось сохранить'
    print(f"[ALL] Формирование одного файла: {status}")
    

    
async def main():
    os.system("cls || clear")

    print('[START] Программа успешно запущена')
    
    await show_settings()

    await app.start()
    await collect_messages()

    input("\n\n[END] Нажмите Enter, для выхода из программы...")



if __name__ == "__main__":
    asyncio.run(main())