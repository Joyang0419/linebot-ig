from fastapi import FastAPI
from src.configs.config import Settings
from src.routers import line_bot


SETTINGS = Settings()


def create_app() -> FastAPI:
    # create FastAPI
    application = FastAPI(
        title=SETTINGS.app_config.title,
        version=SETTINGS.app_config.version,
        debug=SETTINGS.app_config.debug
    )

    # add router to application
    application.include_router(line_bot.router)

    return application


app = create_app()
