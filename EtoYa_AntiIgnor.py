from telethon import TelegramClient, errors, types
from telethon.tl.functions.messages import SendReactionRequest
import asyncio

#реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)
#Введите свои данные через input или удалите input и введите их вручную
api_id = input("Введите api_id: ")
api_hash = input("Введите api_hash: ")

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

async def send_multiple_messages(chat_id, message, count):
    for _ in range(count):
        try:
            await client.send_message(chat_id, message)
            #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
            print(f"Сообщение отправлено в {chat_id}: {message}")
        except errors.RPCError as e:
            print(f"Ошибка при отправке сообщения: {e}")
    print("Все сообщения отправлены.")

async def reply_to_keyword(chat_id, message, keyword):
    async for msg in client.iter_messages(chat_id):
        if keyword in msg.message:
            try:
                await client.send_message(chat_id, message, reply_to=msg.id)
                #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
                print(f"Сообщение '{message}' отправлено в ответ на сообщение с ключевым словом '{keyword}'")
            except errors.RPCError as e:
                print(f"Ошибка при отправке сообщения: {e}")

async def spam(chat_id, message):
    entity = await client.get_entity(chat_id)
    while True:
        try:
            await client.send_message(entity, message)
            #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
            print(f"Сообщение отправлено в {chat_id}: {message}")
        except errors.RPCError as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def send_reactions(chat_id, reaction, user_choice):
    async for message in client.iter_messages(chat_id):
        if not user_choice or message.sender_id == int(user_choice):
            try:
                await client(SendReactionRequest(peer=chat_id, msg_id=message.id, reaction=[types.ReactionEmoji(emoticon=reaction)]))
                #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
                print(f"Реакция '{reaction}' установлена на сообщение {message.id} в чате {chat_id}")
            except errors.RPCError as e:
                print(f"Ошибка при установке реакции: {e}")

async def send_reactions_by_keyword(chat_id, reaction, keyword):
    async for message in client.iter_messages(chat_id):
        if message.message and keyword in message.message:
            try:
                await client(SendReactionRequest(peer=chat_id, msg_id=message.id, reaction=[types.ReactionEmoji(emoticon=reaction)]))
                #Если будут сбои, то добавьте коментарий (символ #) в строке ниже для оптимизации
                print(f"Реакция '{reaction}' установлена на сообщение {message.id} с ключевым словом '{keyword}' в чате {chat_id}")
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
    print("реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)")
    mode = input("Введите номер режима: ")

    tasks = []

    if mode == '1' or mode == '3':
        print("Выберите режим:")
        print("1 - Отправка сообщений с таймером")
        print("2 - Отправка определенного количества сообщений")
        print("3 - Отправка сообщения в ответ на другое сообщение, содержащее выбранное слово")
        print("4 - Спам без остановки")
        print("реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)")
        m = input("Введите номер режима: ")

        if m == '1':
            message = input("Введите сообщение: ")
            try:
                interval = float(input("Введите интервал отправки сообщений (в секундах): "))
            except ValueError:
                print("Неверный формат интервала.")
                return
            tasks.append(send_messages(chat_id, message, interval))

        elif m == '2':
            message = input("Введите сообщение: ")
            try:
                count = int(input("Введите количество сообщений: "))
            except ValueError:
                print("Неверный формат количества.")
                return
            tasks.append(send_multiple_messages(chat_id, message, count))
                
        elif m == '3':
            message = input("Введите сообщение: ")
            keyword = input("Введите ключевое слово: ")
            tasks.append(reply_to_keyword(chat_id, message, keyword))
        
        elif m == '4':
            message = input("Введите сообщение: ")
            tasks.append(spam(chat_id, message))

    if mode == '2' or mode == '3':
        print("Выберите реакцию:")
        print("1 - 👍")
        print("2 - ❤️")
        print("3 - 🤣")
        print("4 - 💋")
        print("5 - 🔥")
        print("6 - 👏")
        print("7 - 💩")
        print("8 - 🎉")
        reaction_choice = input("Введите номер реакции: ")
        reactions = {'1': '👍', '2': '❤️', '3': '🤣', '4': '💋', '5': '🔥', '6': '👏', '7': '💩', '8': '🎉'}
        reaction = reactions.get(reaction_choice, '👍')

        print("Выберите режим:")
        print("1 - По ID пользователя или все сообщения")
        print("2 - По ключевому слову")
        print("реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)")
        rm = input("Введите номер режима: ")

        if rm == '1':
            user_choice = input("Введите ID пользователя или оставьте пустым для всех сообщений: ")
            tasks.append(send_reactions(chat_id, reaction, user_choice))

        elif rm == '2':
            keyword = input("Введите ключевое слово: ")
            tasks.append(send_reactions_by_keyword(chat_id, reaction, keyword))

    await asyncio.gather(*tasks)

#реклама - https://t.me/+nwD-SFfQG3U1ODMy (канал создателя бота)
try:
    with client:
        client.loop.run_until_complete(main())
except KeyboardInterrupt:
    print("Программа завершена.")
