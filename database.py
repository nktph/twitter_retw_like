from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

db = SqliteQueueDatabase('database.db')


class Accounts(Model):
    login = CharField()
    password = CharField()
    mail = CharField()
    mail_password = CharField()


    class Meta:
        db_table = 'Accounts'
        database = db


def connect():
    db.connect()
    Accounts.create_table()
