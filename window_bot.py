"""
Telegram-бот "Расчёт стоимости окон"
=====================================

Что делает:
  1. По команде /start показывает кнопку, открывающую калькулятор
     (Telegram Mini App) прямо внутри Telegram.
  2. Когда клиент заполняет калькулятор и нажимает "Отправить заявку",
     Telegram присылает боту данные — бот форматирует их и пересылает
     менеджеру (ADMIN_CHAT_ID), плюс подтверждает клиенту.

Перед запуском:
  1. Установите зависимости:
       pip install aiogram --break-system-packages

  2. Получите токен бота у @BotFather в Telegram (команда /newbot).

  3. Разместите файл window-calculator.html на своём HTTPS-хостинге
     (GitHub Pages, Netlify, Vercel, свой сервер — подходит любой,
     главное чтобы адрес начинался с https://). Из превью в чате Claude
     ссылку тоже можно использовать для демонстрации, но там раздел
     Telegram (отправка заявки прямо в бота) может работать в
     ограниченном режиме — см. заметку в конце файла.

  4. Впишите ниже:
       BOT_TOKEN      — токен от @BotFather
       WEBAPP_URL     — https://heroic-heliotrope-1c15e3.netlify.app
       ADMIN_CHAT_ID  — 275264199

  5. Запустите:
       python window_bot.py
"""

import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

# ------------------------- НАСТРОЙКИ (заполните свои) -------------------------
BOT_TOKEN = "8934537611:AAHNAh4V51lBJcLSo5VPvOSB-WMCdCb8MxA"
WEBAPP_URL = "https://heroic-heliotrope-1c15e3.netlify.app"
ADMIN_CHAT_ID = 275264199
# --------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🪟 Рассчитать стоимость окна",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(
        "Здравствуйте! Нажмите кнопку ниже, чтобы за пару минут "
        "рассчитать примерную стоимость окна — ответьте на несколько "
        "вопросов, и мы свяжемся с вами по итогам.",
        reply_markup=keyboard,
    )


@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Приходит, когда клиент нажал 'Отправить заявку' в калькуляторе."""
    try:
        data = json.loads(message.web_app_data.data)
    except (ValueError, TypeError):
        await message.answer("Не удалось прочитать расчёт, попробуйте ещё раз.")
        return

    options = ", ".join(data.get("options", [])) or "—"
    lead_text = (
        "🪟 <b>Новая заявка на расчёт окна</b>\n\n"
        f"Клиент: {data.get('name', '—')}\n"
        f"Телефон: {data.get('phone', '—')}\n"
        f"Telegram: @{message.from_user.username or message.from_user.id}\n\n"
        f"Размер: {data.get('width')}×{data.get('height')} мм\n"
        f"Створок: {data.get('sashCount')}, открывание: {data.get('opening')}\n"
        f"Профиль: {data.get('profile')}\n"
        f"Стеклопакет: {data.get('glass')}\n"
        f"Доп. опции: {options}\n"
        f"Количество окон: {data.get('qty')}\n\n"
        f"<b>Итого: {data.get('total'):,} ₽</b>".replace(",", " ")
    )

    if ADMIN_CHAT_ID:
        await bot.send_message(ADMIN_CHAT_ID, lead_text)

    await message.answer(
        "Спасибо! Заявка передана менеджеру — мы свяжемся с вами "
        "по указанному телефону, чтобы уточнить детали и назначить замер."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# --------------------------------------------------------------------------
# Заметка про Telegram-скрипт и хостинг:
#
# Калькулятор (window-calculator.html) подключает официальный скрипт
# https://telegram.org/js/telegram-web-app.js — именно он даёт кнопке
# "Отправить заявку" возможность передать данные прямо в бота (sendData).
# Он должен спокойно загрузиться на вашем собственном хостинге.
# В превью-ссылке из чата Claude загрузка внешних скриптов ограничена
# в целях безопасности, поэтому там калькулятор считает стоимость
# и показывает результат, но саму отправку в бота стоит проверять
# уже после того, как вы разместите файл на своём https-адресе.
# --------------------------------------------------------------------------
