from app import create_app
from decouple import config
from app.config import DevConfig


if __name__ == "__main__":
    create_app()

    