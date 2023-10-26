import os


class Config(object):
    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")

        for var in vars(self):
            if self.__getattribute__(var) is None:
                raise ValueError(f"config: переменная '{var}' должна быть установлена в окружении")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
