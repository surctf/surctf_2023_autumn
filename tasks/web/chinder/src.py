from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardButton, CallbackQuery
from jinja2 import Environment
from database import get_next_card, get_flag, like_card, get_user_card_and_update_photo, Card, update_user, dislike_card
from config import Config
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

cfg = Config()

bot = Bot(token=cfg.BOT_TOKEN)
dp = Dispatcher()

jinja_env = Environment()
jinja_env.filters["get_flag"] = get_flag

CARD_TEMPLATE = """
🇨🇳 <b>{name}</b>

<i> {bio} </i>

❤️ {likes}
"""


@dp.message(Command("start"))
async def start(msg: types.Message):
    f = FSInputFile("chinder.jpg", filename="chinder.jpg")
    await msg.answer_photo(photo=f, caption=("Привет! Это приложение телеграм бот поиск трудовой партнер китай!\n\n"
                                             "Анкета кандитат смотреть начать отправь - /search\n"
                                             "Моя анкета смотреть отправь - /me\n"))


@dp.message(Command("search"))
async def next_card(msg: types.Message):
    usr_id: int = msg.from_user.id

    card = await get_next_card(usr_id)
    f = FSInputFile(card.photo, filename="photo.jpg")

    answ = jinja_env.from_string(
        CARD_TEMPLATE.format(
            name=card.name,
            bio=card.bio,
            likes=card.likes
        )
    )

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="👎", callback_data=f"dislike {card.id}"))
    keyboard.add(InlineKeyboardButton(text="❤️", callback_data=f"like {card.id}"))

    await msg.answer_photo(
        photo=f,
        caption=answ.render(name=card.name, bio=card.bio),
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )


@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    action, card_id = call.data.split()
    if action == "dislike":
        await dislike_card(call.from_user, card_id)

        card = await get_next_card(call.from_user.id)
        f = FSInputFile(card.photo, filename="photo.jpg")

        answ = jinja_env.from_string(
            CARD_TEMPLATE.format(
                name=card.name,
                bio=card.bio,
                likes=card.likes
            )
        )

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="👎", callback_data=f"dislike {card.id}"))
        keyboard.add(InlineKeyboardButton(text="❤️", callback_data=f"like {card.id}"))

        await call.message.answer_photo(
            photo=f,
            caption=answ.render(name=card.name, bio=card.bio),
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )

    elif action == "like":
        card_username, is_match = await like_card(call.from_user, card_id)
        if is_match:
            await call.message.answer(f"МЭТЧ!!!!! ПИСАТЬ СЮДА @{card_username}")
            return

        card = await get_next_card(call.from_user.id)
        f = FSInputFile(card.photo, filename="photo.jpg")

        answ = jinja_env.from_string(
            CARD_TEMPLATE.format(
                name=card.name,
                bio=card.bio,
                likes=card.likes
            )
        )

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="👎", callback_data=f"dislike {card.id}"))
        keyboard.add(InlineKeyboardButton(text="❤️", callback_data=f"like {card.id}"))

        await call.message.answer_photo(
            photo=f,
            caption=answ.render(name=card.name, bio=card.bio),
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )


@dp.message(Command("me"))
async def me(msg: types.Message):
    user_photo = (await msg.from_user.get_profile_photos(limit=1)).photos[0][0].file_id
    await update_user(msg.from_user)

    user_card: Card = await get_user_card_and_update_photo(msg.from_user, user_photo)

    answ = jinja_env.from_string(
        CARD_TEMPLATE.format(
            name=user_card.name,
            bio=user_card.bio,
            likes=user_card.likes
        )
    )

    await msg.answer_photo(
        photo=user_card.photo,
        caption=answ.render(),
        parse_mode="HTML"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
