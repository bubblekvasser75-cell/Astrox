"""
LEAN HOUSE — Telegram bot для запуска мини-аппа (краш-игра со стаканом).

Установка:
    pip install aiogram==3.13.1

Запуск:
    BOT_TOKEN=123:ABC  WEBAPP_URL=https://your-host/index.html  python bot.py

Где:
    BOT_TOKEN   — токен от @BotFather
    WEBAPP_URL  — публичный HTTPS-адрес, где лежит index.html
                  (GitHub Pages / Netlify / Vercel / свой сервер с SSL)
ВАЖНО: Web App открывается ТОЛЬКО по https:// (не http, не file://).
"""
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    MenuButtonWebApp,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT-YOUR-TOKEN-HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-host.example/index.html")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    # 1) Инлайн-кнопка, открывающая Web App поверх чата
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🥤 Играть в LEAN HOUSE",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ]]
    )
    # 2) Кнопка внизу экрана (reply keyboard)
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="🎮 Открыть игру",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ]],
        resize_keyboard=True,
    )
    await message.answer(
        "<b>LEAN HOUSE 🥤</b>\n\n"
        "Краш-игра: стакан летит вверх и множитель растёт. "
        "Успей забрать монеты LH, пока он не разлился!\n\n"
        "Нажми кнопку ниже 👇",
        reply_markup=inline_kb,
    )
    await message.answer("Или открой через кнопку меню снизу:", reply_markup=reply_kb)


# Приём данных из Web App (если в игре вызвать tg.sendData(...))
@dp.message(F.web_app_data)
async def on_webapp_data(message: Message):
    await message.answer(f"📩 Получено из игры: <code>{message.web_app_data.data}</code>")


async def main():
    # Ставим кнопку-меню рядом с полем ввода (синяя кнопка Web App)
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Играть", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    print("Bot started. WebApp:", WEBAPP_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
