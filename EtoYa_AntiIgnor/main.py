from telethon import TelegramClient, errors, types
from telethon.tl.functions.messages import SendReactionRequest
import asyncio
import config as cfg

api_id = cfg.API_ID
api_hash = cfg.API_HASH

client = TelegramClient('session_name', api_id, api_hash)


async def send_messages(chat_id, message, interval):
    while True:
        try:
            await client.send_message(chat_id, message)
            #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
            print(f"Сообщение отправлено в {chat_id}: {message}")
        except errors.RPCError as e:
            print(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(interval)


async def send_reactions(chat_id, reaction, user_choice):
    async for message in client.iter_messages(chat_id):
        if not user_choice or message.sender_id == int(user_choice):
            try:
                await client(SendReactionRequest(peer=chat_id, msg_id=message.id, reaction=[types.ReactionEmoji(emoticon=reaction)]))
                #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
                print(f"Реакция '{reaction}' установлена на сообщение {message.id} в чате {chat_id}")
            except errors.RPCError as e:
                print(f"Ошибка при установке реакции: {e}")


async def main():
    try:
        await client.start()
        print("реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)")
    except errors.RPCError as e:
        print(f"Ошибка при подключении: {e}")
        return

    async for dialog in client.iter_dialogs():
        print(dialog.name, '-', dialog.id)

    chat_id = input("Введите имя чата: ")

    try:
        await client.get_entity(chat_id)
    except ValueError:
        print(f"Чат с ID или именем '{chat_id}' не найден.")
        return

    print("Выберите режим:")
    print("1 - Отправка сообщений")
    print("2 - Установка реакций")
    print("3 - Комбинированный режим")
    mode = input("Введите номер режима: ")

    tasks = []

    if mode == '1' or mode == '3':
        message = input("Введите сообщение: ")
        try:
            interval = float(input("Введите интервал отправки сообщений (в секундах): "))
        except ValueError:
            print("Неверный формат интервала.")
            return
        tasks.append(send_messages(chat_id, message, interval))

    if mode == '2' or mode == '3':
        print("Выберите реакцию:")
        print("1 - 👍")
        print("2 - ❤️")
        print("3 - 🤣")
        print("4 - 💋")
        print("5. 🔥")
        print("6. 👏")
        print("7. 💩")
        print("8. 🎉")
        reaction_choice = input("Введите номер реакции: ")
        reactions = {'1': '👍', '2': '❤️', '3': '🤣', 4: '💋', "5": "🔥", "6": "👏", "7": "💩", "8": "🎉"}
        reaction = reactions.get(reaction_choice, '👍')

        user_choice = input("Введите ID пользователя или оставьте пустым для всех сообщений: ")
        tasks.append(send_reactions(chat_id, reaction, user_choice))

    await asyncio.gather(*tasks)


try:
    with client:
        client.loop.run_until_complete(main())
except KeyboardInterrupt:
    print("Программа завершена.")
