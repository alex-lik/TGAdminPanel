from os import getenv

from dotenv import load_dotenv

if not getenv("SQLALCHEMY_DATABASE_URL"):
    load_dotenv()


SQLALCHEMY_DATABASE_URL = getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./telegram_content.db")

LOG_PATH = './logs/today.log'


