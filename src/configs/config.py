from pathlib import Path

from pydantic import BaseSettings


class ReadEnv(BaseSettings):

    class Config:
        env_file = Path(__file__) \
            .resolve().parent.parent.parent.joinpath(".env")
        env_file_encoding = 'utf-8'


class LineBotConfig(ReadEnv):
    channel_secret: str
    channel_access_token: str


class ApplicationConfig(ReadEnv):
    title: str = 'LineBot IG Photo response'
    version: str = '0.1.0'
    debug: bool = True


class InstagramAccount(ReadEnv):
    ig_account: str
    ig_password: str


class Settings(BaseSettings):
    app_config: ApplicationConfig = ApplicationConfig()
    line_bot_config: LineBotConfig = LineBotConfig()
    ig_account_config: InstagramAccount = InstagramAccount()
