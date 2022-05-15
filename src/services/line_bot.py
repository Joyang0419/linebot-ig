import glob
import pathlib

from linebot.models import (
    TextSendMessage, ImageSendMessage
)

from src.configs.config import Settings
from src.services.ig_crawler import ServiceInstagramScraper
from random import choice
import json
import threading

IG_ACCOUNT_CONFIG = Settings().ig_account_config
PHOTOS_PATH = \
    pathlib.Path(__file__).parent.parent.parent.resolve().joinpath('photos')


class ServiceLineBot:

    @staticmethod
    def execute_action(message: str):

        message_parser = message.split(' ', 1)
        action_str = message_parser[0]

        if len(message_parser) == 2:
            if action_str == 'get':
                account = message_parser[1]
                action = ServiceLineBot.actions_menu(action=action_str)
                return action(account=account)
        else:
            action = ServiceLineBot.actions_menu(action=message)
            if action:
                return action()

    @staticmethod
    def actions_menu(action: str):
        actions = {
            'mei mei': ServiceLineBot.give_mei_mei,
            'help': ServiceLineBot.help_message,
            'get': ServiceLineBot.active_start_crawl
        }

        return actions.get(action)

    @staticmethod
    def active_start_crawl(account: str) -> list:
        service = ServiceInstagramScraper(
            account=IG_ACCOUNT_CONFIG.ig_account,
            password=IG_ACCOUNT_CONFIG.ig_password,
            get_media_types=['image'],
            get_chunk_size=100
        )

        sub_process = threading.Thread(
            target=service.start_crawl,
            args=[account]
        )
        sub_process.start()

        return [TextSendMessage(text=f'start_crawl: {account}')]

    @staticmethod
    def give_mei_mei() -> list:
        files = glob.glob(f"{PHOTOS_PATH}/*.txt")
        selected_file = choice(files)

        with open(
                file=selected_file,
                mode='r'
        ) as f:
            text = f.read()
            data: dict = json.loads(text)

        ig_shortcode = choice(list(data.keys()))
        ig_display_url = data.pop(ig_shortcode)

        with open(
            file=selected_file,
            mode='w'
        ) as f:
            f.write(json.dumps(data))

        return [
            ImageSendMessage(
                original_content_url=ig_display_url,
                preview_image_url=ig_display_url
            ),
            TextSendMessage(text=f'https://www.instagram.com/p/{ig_shortcode}/')
        ]

    @staticmethod
    def help_message():
        help_message_content = """
        mei mei: give one mei mei photo and url.
        get <ig_account>: get images from ig_account, but don't provide image 
        right now, next time mei mei have change to choose it to send you.
        """
        return [
            TextSendMessage(text=help_message_content)
        ]
