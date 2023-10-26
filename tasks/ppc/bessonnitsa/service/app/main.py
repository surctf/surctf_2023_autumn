# -*- coding: utf-8 -*-
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from jinja2 import Environment, FileSystemLoader, select_autoescape

from random import choice
from typing import List

from .config import ANIMAL_COUNT, FLAG


app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

env = Environment(
    loader=FileSystemLoader('app/templates'),
    autoescape=select_autoescape(['html', 'xml', 'css'])
)
env.globals['STATIC_PREFIX'] = 'static/'

possible_animals = ["🐺", "🐺", "🐑", "🐑", "🐑"]


def send_animal(msg):
    template = env.get_template('message.html')
    message = template.render(msg=msg)
    return message


@app.get('/')
async def index():
    template = env.get_template('index.html')
    return HTMLResponse(template.render())


@app.websocket('/ws/{client_id}')
async def ws(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "Connected":
                animal_list = [choice(possible_animals) for i in range(ANIMAL_COUNT)]
                chosen_animal = choice(["🐺", "🐑"])
                answer = animal_list.count(chosen_animal)
                for animal in animal_list:
                    await manager.send_personal_message(send_animal(msg=animal), websocket)
                    await asyncio.sleep(0.5)
                if chosen_animal == "🐺":
                    message = "Сколько волков вы насчитали?"
                elif chosen_animal == "🐑":
                    message = "Сколько овeц вы насчитали?"
                await manager.send_personal_message(send_animal(msg=message), websocket)
            elif data == str(answer):
                await manager.send_personal_message(send_animal(msg=FLAG), websocket)
                raise WebSocketDisconnect
            else:
                await manager.send_personal_message(send_animal(msg="НЕУДАЧА"), websocket)
                raise WebSocketDisconnect
    except WebSocketDisconnect:
        manager.disconnect(websocket)
