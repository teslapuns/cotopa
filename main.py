import os
import random
import sqlite3
from vkbottle.bot import Bot, Message
from vkbottle import API

token = os.environ['token']
interval = random.randint(20, 50)
counter = 0

bot = Bot(token=token)
api = API(token=token)

conn = sqlite3.connect('messages.db')
conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)')


@bot.on.chat_message()
async def handle_message(message: Message):
    if (len(message.text) > 30):
        return
    
    global counter

    with sqlite3.connect('messages.db') as conn:
        conn.execute('INSERT INTO messages (text) VALUES (?)', (message.text,))

        counter += 1

        if counter == interval:
            cursor = conn.execute('SELECT text FROM messages ORDER BY RANDOM() LIMIT 1')
            random_message = next(cursor)[0]

            await bot.api.messages.send(
                message=random_message,
                random_id=random.randint(1, 2 ** 31),
                peer_id=message.peer_id,
            )

            counter = 0


def main():
    bot.run_forever()


if __name__ == '__main__':
    main()
