import base64
import json
import os
import random
import sys

QUESTIONS_DIR = "questions"

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("Переменная окружения 'FLAG' не установлена!")


def check_is_xy_in_box(x: int, y: int, box: list) -> bool:
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


questions = os.listdir(QUESTIONS_DIR)
questions = list(filter(lambda f: not f.startswith("._"), questions))

random.shuffle(questions)

total_count = len(questions)

print("""
Привет, можешь помочь мне найти человека на картинке? А я тебе за это дам флаг.
Я отправлю тебе картинку, а ты ответь мне координатами XY обозначающими где находится человек на картинке.
X, Y - целые числа;
X - столбец изображения 0-255 (слева на право);
Y - строка изображения 0-255 (сверху вниз);
X и Y отправляй разделенными пробелом;

Для примера:
124 126
Здесь X=124, Y=126

Если на картинке несколько человек, отправляй координату любого из них;
Если на картинке нет людей, отправь 'no person' (без ковычек);
""")

input("Чтобы начать жми [ENTER]!")

good = 0
for q in questions:
    with open(os.path.join(QUESTIONS_DIR, q), "r") as f:
        q = json.loads(f.read())
    # with open(os.path.join(QUESTIONS_DIR, q_img), "rb") as f:
    #     img_base = base64.b64encode(f.read())
    #
    # a_json, _ = os.path.splitext(q_img)
    # a_json = a_json + ".json"
    # with open(os.path.join(ANSWERS_DIR, a_json), "r") as f:
    #     a_json = json.loads(f.read())
    #
    print(f"IMG: {q['image']}")

    answ = input("ANSW: ")
    if answ == "no person":
        if len(q["persons"]) == 0:
            print("good")
            good += 1
            continue
        else:
            print("bad")
            continue

    try:
        x, y = map(int, answ.split())
    except Exception as e:
        print("Invalid answer format, bye!")
        sys.exit()

    is_good = False
    for box in q["persons"]:
        is_good = check_is_xy_in_box(x, y, box)
        if is_good:
            break

    if is_good:
        good += 1
        print("good")
    else:
        print("bad")

good_answ_rate = (good / total_count) * 100
if good_answ_rate < 85:
    print(
        f"Ты допустил слишком много ошибок, всего {good_answ_rate:.1f}% "
        f"верных ответов, за такое даже стыдно давать флаг..."
    )
else:
    print(
        f"Отлично! Целых {good_answ_rate:.1f}% правильных ответов, вот твой флаг"
        f": \n{FLAG}"
    )
