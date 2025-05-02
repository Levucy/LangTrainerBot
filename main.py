from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import sqlite3


words = {
    "apple": "яблоко",
    "banana": "банан",
    "beautiful": "красивый",
    "big": "большой",
    "bird": "птица",
    "book": "книга",
    "car": "машина",
    "cat": "кошка",
    "city": "город",
    "cold": "холодный",
    "computer": "компьютер",
    "dog": "собака",
    "door": "дверь",
    "fast": "быстрый",
    "fish": "рыба",
    "friend": "друг",
    "good": "хороший",
    "grape": "виноград",
    "happy": "счастливый",
    "hot": "горячий",
    "house": "дом",
    "key": "ключ",
    "light": "свет",
    "moon": "луна",
    "music": "музыка",
    "new": "новый",
    "orange": "апельсин",
    "pen": "ручка",
    "phone": "телефон",
    "rabbit": "кролик",
    "rain": "дождь",
    "sad": "грустный",
    "school": "школа",
    "slow": "медленный",
    "small": "маленький",
    "sun": "солнце",
    "time": "время",
    "tree": "дерево",
    "water": "вода",
    "watermelon": "арбуз",
    "window": "окно",
    "work": "работа",
    "world": "мир",
    "year": "год"
}


async def start(update, context):
    await update.message.reply_text("Привет! Я бот для изучения английских слов.\n""Используй команды:\n"
        "/start - начать\n""/learn - показать случайное слово\n""/quiz - начать викторину")


async def learn(update, context):
    word, translation = random.choice(list(words.items()))
    await update.message.reply_text(f"{word} - {translation}")


async def quiz(update, context):
    user = update.message.from_user.username
    streak = 0
    # print(user)
    word, translation = random.choice(list(words.items()))

    if user:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT username FROM streak WHERE username = ?", (user,))
        for a in db2:
            if a[0] != user:
                db1.execute("INSERT INTO streak(username, streak) VALUES(?, ?)", (user, streak))
            else:
                db1.execute("UPDATE streak SET lastword = ? WHERE username = ?", (word, user))
        # print(db2)
        # db1.execute("INSERT INTO streak(username, streak) VALUES(?, ?)", (user, streak))
        db.commit()
        db.close()

        await update.message.reply_text(f"Как переводится слово {word}?")
    else:
        await update.message.reply_text(f"Чтобы использовать данную команду, вам необходимо иметь username.")


async def quiz_answer(update, context):
    user = update.message.from_user.username
    streak = 0
    message = update.message.text
    word = ''

    if user:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT lastword FROM streak WHERE username = ?", (user,))
        for a in db2:
            word = a[0]
        if message == word:
            await update.message.reply_text(f"Это правильный ответ!\nВы верно угадали {streak} слов!")
        else:
            await update.message.reply_text(f"Ответ неверный, {word} переводится как {words[word]}.")


async def unknown(update, context):
    await update.message.reply_text("Неизвестная команда. Используйте /start.")


def main() -> None:
    application = Application.builder().token("7999823112:AAHyysck9NAuPL2D5LY2rjOBE8LmFHUAtq4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(MessageHandler(filters.TEXT, quiz_answer))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()


if __name__ == "__main__":
    main()