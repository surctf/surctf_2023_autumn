from pathlib import Path
from typing import Union, Any

from aiogram.types import User
import random
import os

from config import Config

SCRIPT_DIR = Path(__file__).parent

with open(os.path.join(SCRIPT_DIR, "pasta.txt"), "r") as f:
    pasta = f.read().replace("\n", " ").lower()

words = pasta.split(" ")

with open(os.path.join(SCRIPT_DIR, "femail_names.txt"), "r") as f:
    female_names = f.read().split("\n")

with open(os.path.join(SCRIPT_DIR, "male_names.txt"), "r") as f:
    male_names = f.read().split("\n")

photos = os.listdir(os.path.join(SCRIPT_DIR, "photos"))

cfg = Config()


def get_flag(*args) -> str:
    return cfg.FLAG


def _get_card_bio(r: Union[random.Random, Any] = random):
    bio = ""
    for j in range(6):
        part_len = r.randint(3, 8)
        start = r.randint(0, len(words) - part_len - 1)
        bio = bio + " ".join(words[start:start + part_len]) + " "
    bio = bio.capitalize()[:-1] + "!"

    return bio


def _get_card_name(is_male: bool, r: Union[random.Random, Any] = random):
    return r.choice(male_names) if is_male else r.choice(female_names)


def _get_card_photo(r: Union[random.Random, Any] = random) -> (str, bool):
    """
    returns (path: str, is_male: bool)
    """

    photo = r.choice(photos)
    return os.path.join(
        os.path.join(SCRIPT_DIR, "photos"), photo
    ), photo.startswith("male")


class Card:
    def __init__(self, r: Union[random.Random, Any] = random):
        self.id = r.randint(1000000, 100000000)
        self.photo, self.is_male = _get_card_photo(r)
        self.name = _get_card_name(self.is_male, r)
        self.bio = _get_card_bio(r)
        self.likes = r.randint(10, 77)
        self.username = "unkown"


async def get_next_card(*args) -> Card:
    return Card()


async def update_user(*args):
    pass


async def get_user_card_and_update_photo(user: User, photo) -> Card:
    rng = random.Random(user.id)

    card = Card(rng)
    card.id = user.id
    card.name = user.first_name
    card.photo = photo

    return card


async def like_card(*args) -> (None, bool):
    return (None, False)


async def dislike_card(*args):
    pass
