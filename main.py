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
    "car": ["машина", "автомобиль"],
    "cat": ["кошка", "кот"],
    "city": "город",
    "cold": "холодный",
    "computer": "компьютер",
    "dog": ["собака", "пес"],
    "door": "дверь",
    "fast": "быстрый",
    "fish": "рыба",
    "friend": "друг",
    "good": "хороший",
    "grape": "виноград",
    "happy": ["счастливый", "радостный", "веселый"],
    "hot": "горячий",
    "house": "дом",
    "key": "ключ",
    "light": "свет",
    "moon": "луна",
    "music": "музыка",
    "new": "новый",
    "orange": ["апельсин", "оранжевый"],
    "pen": "ручка",
    "phone": "телефон",
    "rabbit": ["кролик", "заяц"],
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
    count = 0
    print([user])
    word, translation = random.choice(list(words.items()))

    if len(user) > 0:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT username FROM streak WHERE username = ?", (user,))
        for a in db2:
            count += 1
        if count == 0:
            print(f'{user} was added to the database')
            db1.execute("INSERT INTO streak(username, streak, lastword, quizzing) VALUES(?, ?, ?, ?)",
                        (user, streak, word, 1))
        else:
            print(f'{user} used /quiz command')
            db1.execute("UPDATE streak SET lastword = ? WHERE username = ?", (word, user))
            db1.execute("UPDATE streak SET quizzing = 1 WHERE username = ?", (user,))
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
    quizzing = 0
    translation = ''
    print([user, message])

    if user:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT streak, lastword, quizzing FROM streak WHERE username = ?", (user,))
        for a in db2:
            streak = int(a[0])
            word = a[1]
            translation = words[word]
            quizzing = int(a[2])
        # print([user, streak, word, translation, message, quizzing])
        if quizzing == 1:
            db1.execute("UPDATE streak SET quizzing = 0 WHERE username = ?", (user,))
            if quiz_answer_check(word, translation): # message.lower() == translation:
                db1.execute("UPDATE streak SET streak = ? WHERE username = ?", (streak + 1, user))
                await update.message.reply_text(f"Это правильный ответ!\nВы верно угадали {streak + 1} слов!")
            else:
                db1.execute("UPDATE streak SET streak = 0 WHERE username = ?", (user,))
                await update.message.reply_text(f"Ответ неверный, {word} переводится как {translation}.")
        db.commit()
        db.close()


async def quiz_answer_check(word, translation):
    translation = translation.replace("ё", "е")
    symbols = ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы", "в", "а", "п", "р", "о", "л", "д",
               "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю"]
    if translation in words[word]:
        return True
    if translation[-2:] in ["ый", "ое", "ая"]:
        return True
    return False


async def unknown(update, context):
    await update.message.reply_text("Неизвестная команда. Используйте /start.")


def main() -> None:
    application = Application.builder().token("7999823112:AAGc6zD2L0mrGjuIUzFMuTNiEEVaWi_KUDY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(MessageHandler(filters.TEXT, quiz_answer))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()


if __name__ == "__main__":
    main()