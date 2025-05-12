from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import sqlite3


words = {
    "animal": ["животное"],
    "apple": ["яблоко"],
    "baby": ["ребенок", "младенец"],
    "ball": ["мяч"],
    "banana": ["банан"],
    "beautiful": ["красивый"],
    "bed": ["кровать"],
    "big": ["большой"],
    "bird": ["птица"],
    "book": ["книга"],
    "brother": ["брат"],
    "car": ["машина", "автомобиль"],
    "cat": ["кошка", "кот"],
    "chair": ["стул"],
    "child": ["ребенок"],
    "city": ["город"],
    "cloud": ["облако"],
    "cold": ["холодный"],
    "computer": ["компьютер"],
    "dance": ["танец"],
    "dark": ["темный"],
    "day": ["день"],
    "doctor": ["врач", "доктор"],
    "dog": ["собака", "пес"],
    "door": ["дверь"],
    "earth": ["земля"],
    "eye": ["глаз"],
    "fast": ["быстрый"],
    "father": ["отец", "папа"],
    "fish": ["рыба"],
    "flower": ["цветок"],
    "food": ["еда"],
    "friend": ["друг"],
    "game": ["игра"],
    "girl": ["девочка"],
    "good": ["хороший"],
    "grape": ["виноград"],
    "green": ["зеленый"],
    "hand": ["рука"],
    "happy": ["счастливый", "радостный", "веселый"],
    "head": ["голова"],
    "heart": ["сердце"],
    "home": ["дом", "жилище"],
    "horse": ["лошадь"],
    "hot": ["горячий"],
    "house": ["дом"],
    "ice": ["лед"],
    "key": ["ключ"],
    "king": ["король"],
    "laugh": ["смех"],
    "light": ["свет"],
    "love": ["любовь"],
    "man": ["мужчина"],
    "moon": ["луна"],
    "mother": ["мать", "мама"],
    "music": ["музыка"],
    "new": ["новый"],
    "night": ["ночь"],
    "orange": ["апельсин", "оранжевый"],
    "paper": ["бумага"],
    "peace": ["мир", "покой"],
    "pen": ["ручка"],
    "people": ["люди"],
    "phone": ["телефон"],
    "rabbit": ["кролик", "заяц"],
    "rain": ["дождь"],
    "red": ["красный"],
    "river": ["река"],
    "road": ["дорога"],
    "sad": ["грустный"],
    "school": ["школа"],
    "sea": ["море"],
    "sister": ["сестра"],
    "sky": ["небо"],
    "slow": ["медленный"],
    "small": ["маленький"],
    "snow": ["снег"],
    "star": ["звезда"],
    "street": ["улица"],
    "sun": ["солнце"],
    "sunny": ["солнечный"],
    "teacher": ["учитель"],
    "time": ["время"],
    "toy": ["игрушка"],
    "train": ["поезд"],
    "tree": ["дерево"],
    "watch": ["часы"],
    "water": ["вода"],
    "watermelon": ["арбуз"],
    "window": ["окно"],
    "woman": ["женщина"],
    "work": ["работа"],
    "world": ["мир"],
    "year": ["год"],
    "yellow": ["желтый"]
}


async def start(update, context):
    await update.message.reply_text("Привет! Я бот для изучения английских слов.\n""Используй команды:\n"
        "/leaderboard - вывести таблицу лидеров\n""/learn - показать случайное слово\n""/quiz - начать викторину")


async def learn(update, context):
    word, translation = random.choice(list(words.items()))
    await update.message.reply_text(f"{word} - {', '.join(translation)}")


async def quiz(update, context):
    user = update.message.from_user.username
    streak = 0
    count = 0
    word, translation = random.choice(list(words.items()))
    anti_cheat = False

    if len(user) > 0:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT username, quizzing FROM streak WHERE username = ?", (user,))
        for a in db2:
            if a[1] == 1:
                anti_cheat = True
            count += 1
        if count == 0:
            db1.execute("INSERT INTO streak(username, streak, lastword, quizzing) VALUES(?, ?, ?, ?)",
                        (user, streak, word, 1))
        elif not anti_cheat:
            db1.execute("UPDATE streak SET lastword = ? WHERE username = ?", (word, user))
            db1.execute("UPDATE streak SET quizzing = 1 WHERE username = ?", (user,))
        else:
            db2 = db1.execute("SELECT lastword FROM streak WHERE username = ?", (user,))
            for a in db2:
                word = a[0]
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

    if user:
        db = sqlite3.connect("TelegramBotDB")
        db1 = db.cursor()
        db2 = db1.execute("SELECT streak, lastword, quizzing FROM streak WHERE username = ?", (user,))
        for a in db2:
            streak = int(a[0])
            word = a[1]
            translation = words[word]
            quizzing = int(a[2])
        if quizzing == 1:
            db1.execute("UPDATE streak SET quizzing = 0 WHERE username = ?", (user,))
            if await quiz_answer_check(word, message.lower()): # message.lower() == translation:
                db1.execute("UPDATE streak SET streak = ? WHERE username = ?", (streak + 1, user))
                word_case = 'слов'
                if (streak + 1) % 10 == 1 and streak + 1 != 11:
                    word_case = 'слово'
                elif (streak + 1) % 10 in [2, 3, 4]:
                    word_case = 'слова'
                elif (streak + 1) % 10 >= 5 and str(streak + 1)[0] != '1':
                    word_case = 'слов'
                await update.message.reply_text(f"Это правильный ответ!\nВы верно угадали "
                                                f"{streak + 1} {word_case} подряд!")
            else:
                db1.execute("UPDATE streak SET streak = 0 WHERE username = ?", (user,))
                await update.message.reply_text(f"Ответ неверный, {word} переводится как {', '.join(translation)}.")
        db.commit()
        db.close()


async def quiz_answer_check(word, message):
    message = message.replace("ё", "е")
    if message in words[word]:
        return True
    if (message[-2:] in ["ый", "ое", "ая"] and message[:-2] in ''.join(words[word])[:-2] and
            ''.join(words[word])[-2:] in ["ый", "ое", "ая"]):
        return True
    return False


async def leaderboard(update, context):
    streaks = {}
    leaderboard = []
    db = sqlite3.connect("TelegramBotDB")
    db1 = db.cursor()
    db2 = db1.execute("SELECT username, streak FROM streak WHERE streak > ?", (-1,))
    for a in db2:
        if a[1] not in streaks.keys():
            streaks[a[1]] = [f'@{a[0]}']
        else:
            b = streaks[a[1]]
            b.append(f'@{a[0]}')
            streaks[a[1]] = b
    for i in sorted(streaks.keys(), reverse=True):
        leaderboard.append(f'{i}: {', '.join(streaks[i])}')
    await update.message.reply_text(f"Таблица лидеров\n{'\n'.join(leaderboard)}")


async def unknown(update, context):
    await update.message.reply_text("Неизвестная команда. Используйте /start.")


def main() -> None:
    application = Application.builder().token("7999823112:AAGc6zD2L0mrGjuIUzFMuTNiEEVaWi_KUDY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(MessageHandler(filters.TEXT, quiz_answer))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()


if __name__ == "__main__":
    main()