from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, IntegerField
from typing import List


db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    _id = IntegerField(primary_key=True)
    phone = TextField()


class Password(BaseModel):
    _id = IntegerField(primary_key=True)
    owner_phone = TextField()
    text = TextField()


db.create_tables([User, Password])