import datetime

from peewee import DatabaseProxy, DateTimeField, Model, SqliteDatabase, TextField

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Post(BaseModel):
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)


class Settings(BaseModel):
    key = TextField()
    value = TextField()


def get_posts() -> list[Post]:
    return list(Post.select().order_by(Post.created_date.desc()))


def get_settings() -> Settings:
    return Settings.get(Settings.key == "words_per_day")


def init_db(db_path: str):
    db = SqliteDatabase(db_path)
    database_proxy.initialize(db)

    db.connect()
    db.create_tables([Post, Settings])

    # Initialize settings:
    Settings.get_or_create(key="words_per_day", defaults={"value": "300"})
