from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Увеличенный словарь английских слов
words = {"apple": "яблоко",
         "banana": "банан",
         "orange": "апельсин",
         "grape": "виноград",
         "watermelon": "арбуз",
         "dog": "собака",
         "cat": "кошка",
         "bird": "птица",
         "fish": "рыба",
         "rabbit": "кролик",
         "house": "дом",
         "car": "машина",
         "tree": "дерево",
         "sun": "солнце",
         "moon": "луна",
         "book": "книга",
         "pen": "ручка",
         "computer": "компьютер",
         "phone": "телефон",
         "music": "музыка",
         "happy": "счастливый",
         "sad": "грустный",
         "big": "большой",
         "small": "маленький",
         "fast": "быстрый",
         "slow": "медленный",
         "good": "хороший",
         "bad": "плохой",
         "hot": "горячий",
         "cold": "холодный"}


async def start(update, context):
    await update.message.reply_text("Привет! Я бот для изучения английских слов.\n""Используй команды:\n"
        "/start - начать\n""/learn - показать случайное слово\n""/quiz - начать викторину")


async def learn(update, context):
    word, translation = random.choice(list(words.items()))
    await update.message.reply_text(f"{word} — {translation}")


async def quiz():
    pass


async def unknown(update, context):
    await update.message.reply_text("Неизвестная команда. Используйте /start.")


def main() -> None:
    application = Application.builder().token("7999823112:AAHyysck9NAuPL2D5LY2rjOBE8LmFHUAtq4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("quiz", learn))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()


if __name__ == "__main__":
    main()