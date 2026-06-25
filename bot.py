from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

ADMIN_GROUP_ID = -1003864481386
ADMIN_USERNAME = "@sergiodevv"


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "📋 Для подачи анкеты отправьте:\n\n"
        "1. Имя\n"
        "2. Возраст\n"
        "3. ЮЗ\n"
        "4. Скин (фото)\n\n"
        "После проверки администрацией вам придет ответ."
    )


@dp.message(F.photo)
async def photo_handler(message: Message):
    caption = (
        f"📨 Новая анкета\n\n"
        f"От: @{message.from_user.username or 'нет_username'}\n"
        f"ID: {message.from_user.id}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=f"accept_{message.from_user.id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{message.from_user.id}"
                )
            ]
        ]
    )

    await bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=keyboard
    )

    await message.answer(
        "✅ Анкета отправлена администрации на рассмотрение."
    )


@dp.message()
async def text_handler(message: Message):
    text = (
        f"📨 Новая анкета\n\n"
        f"{message.text}\n\n"
        f"От: @{message.from_user.username or 'нет_username'}\n"
        f"ID: {message.from_user.id}"
    )

    await bot.send_message(
        ADMIN_GROUP_ID,
        text
    )

    await message.answer(
        "✅ Текст анкеты получен. Теперь отправьте фото скина."
    )


@dp.callback_query(F.data.startswith("accept_"))
async def accept(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    await bot.send_message(
        user_id,
        f"✅ Ваша анкета успешно принята.\n\n"
        f"Напишите администратору:\n{ADMIN_USERNAME}"
    )

    await callback.answer("Анкета принята")
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.callback_query(F.data.startswith("reject_"))
async def reject(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[1])

    await bot.send_message(
        user_id,
        "❌ Ваша анкета отклонена администрацией."
    )

    await callback.answer("Анкета отклонена")
    await callback.message.edit_reply_markup(reply_markup=None)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
