import numpy as np
import cv2
from ultralytics import YOLO
import base64
from pwn import *

cv2.startWindowThread() # запускаем поток работающий с окнами в opencv

conn = remote('194.26.138.228', 9050) # подключаемся к сервису

yolo = YOLO("yolov8n.pt") # загружаем модель с помощью которой будем детектить людей

conn.sendline(b"") # отправляем ENTER
print(conn.recvuntil(b"IMG: ").decode("utf-8")) # скипаем весь текст до IMG:

try:
    while True:
        img = conn.recvuntil(b"ANSW: ", drop=True).strip() # получаем base64 картинки
        img = np.frombuffer(base64.b64decode(img), dtype=np.uint8) # декодим base64 и формируем numpy массив
        img = cv2.imdecode(img, cv2.IMREAD_COLOR) # конвертируем numpy массив в картинку

        result = yolo(img, verbose=False)[0] # отправляем картинку на вход нейронке, берем первое предсказание
        boxes = np.array(result.boxes.xyxy, dtype="int") # конвертируем предсказанные боксы numpy массив

        persons = []
        for i, xyxy in enumerate(boxes):
            if result.boxes.cls[i] != 0:  # отбираем только боксы с нулевым классом(класс = 0 - это человек)
                continue

            xyxy = tuple(map(int, xyxy))
            persons.append(xyxy)

            cv2.rectangle(img, xyxy[:2], xyxy[2:], (0, 255, 0), 2) # рисуем боксы на картинке

        if len(persons) == 0:
            answ = b"no person" # если нет боксов с людьми, то формируем ответ 'no person'
        else:
            x = (persons[0][0] + persons[0][2]) // 2
            y = (persons[0][1] + persons[0][3]) // 2
            cv2.circle(img, (x, y), 0, (0, 0, 255), 3)
            answ = f"{x} {y}".encode("utf-8") # иначе формируем ответ с координатами середины первого бокса

        print("SENDING:", answ.decode("utf=8"))
        cv2.imshow("image", img) # рисуем картинку в окне
        k = cv2.waitKey(1) # ожидание(1мс) ввода от юзера, нужно для корректной последователньой отрисовки изображений
        if k & 0xFF == ord("q"): # если нажали 'q' - выходим
            break

        conn.sendline(answ) # отправляем ответ

        print("RESULT:", conn.recvuntil(b"IMG: ").decode("utf-8")) # выводим результат
except Exception as e:
    # если случилась ошибка - переходим в интерактивный режим, для отладки
    # полезно когда не знаешь что может отправить сервис(при успешном проохождении или еще когда)
    conn.interactive()
finally:
    cv2.destroyAllWindows() # закрываем все окна opencv