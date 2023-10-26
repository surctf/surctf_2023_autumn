from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import KeyboardBuilder
from aiogram.types import FSInputFile

from config import Config

import logging
import asyncio

from database import User, Password

logging.basicConfig(level=logging.INFO)

cfg = Config()

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(msg: types.Message):
    user_id = msg.from_user.id
    user: User = User.select().where(User._id == user_id).get_or_none()

    if user is None:
        builder = KeyboardBuilder(button_type=types.KeyboardButton)
        builder.add(types.KeyboardButton(
            text="Авторизоваться",
            request_contact=True),
        )

        f = FSInputFile("logo.jpeg", filename="logo.jpeg")
        await msg.answer_photo(
            photo=f,
            caption="Привет, чтобы авторизоваться тыкни кнопку снизу!",
            reply_markup=builder.as_markup()
        )
        return

    await msg.answer(f"Можешь посмотреть свои пароли /passwords")


@dp.message(Command("add_password"))
async def add_password(msg: types.Message):
    user_id = msg.from_user.id
    user = User.select().where(User._id == user_id).get_or_none()

    if user is None:
        builder = KeyboardBuilder(button_type=types.KeyboardButton)
        builder.add(types.KeyboardButton(
            text="Поделиться контактом",
            request_contact=True),
        )

        await msg.answer(
            "Привет, чтобы авторизоваться отправь мне свой контакт!",
            reply_markup=builder.as_markup()
        )
        return

    passwords_count = Password.select().where(Password.owner_phone == user.phone).count()
    if passwords_count >= 5:
        await msg.answer("Пока бесплатно ты можешь хранить только 5 паролей, если хочешь больше пиши админу: @cooldoor")
        return

    password_text = msg.text[len("/add_password "):]
    if len(password_text) < 8:
        await msg.answer(
            "Нельзя использовать такие простые пароли, напиши хотя бы 8 символов!\n /add_password <пароль>")
        return

    password = Password.create(text=password_text, owner_phone=user.phone)

    return await get_passwords(msg, user)


@dp.message(Command("passwords"))
async def get_passwords(msg: types.Message, user: User = None):
    if user is None:
        user = User.select().where(User._id == msg.from_user.id).get_or_none()

    if user is None:
        builder = KeyboardBuilder(button_type=types.KeyboardButton)
        builder.add(types.KeyboardButton(
            text="Поделиться контактом",
            request_contact=True),
        )

        await msg.answer(
            "Привет, чтобы авторизоваться отправь мне свой контакт!",
            reply_markup=builder.as_markup()
        )
        return

    passwords = list(Password.select().where(Password.owner_phone == user.phone))

    answ = "Ваши пароли:\n"
    for i, password in enumerate(passwords):
        answ += f"    {i + 1}. {password.text}\n"

    await msg.answer(answ)


@dp.message(F.contact)
async def on_contact(msg: types.Message):
    user_id = msg.from_user.id
    user = User.select().where(User._id == user_id).get_or_none()

    phone = msg.contact.phone_number.replace("+", "").replace(" ", "").replace("(", "").replace(")", "")
    if user is None:
        user = User.create(_id=user_id, phone=phone).get_or_none()

    if user is None:
        await msg.answer(f"Какие-то проблемы, пингани @phizog")
        return

    logging.info(phone)

    User.update(phone=phone).where(User._id == user._id).execute()

    await msg.answer(f"Авторизован! Можешь посмотреть свои пароли /passwords")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
