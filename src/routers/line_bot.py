import aiohttp
from fastapi import APIRouter
from fastapi import Request, HTTPException
from linebot import (
    AsyncLineBotApi, WebhookParser
)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageSendMessage,
)

from src.services.line_bot import ServiceLineBot

from src.configs.config import Settings

SETTINGS = Settings()

router = APIRouter()

session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(
    SETTINGS.line_bot_config.channel_access_token,
    async_http_client
)
parser = WebhookParser(SETTINGS.line_bot_config.channel_secret)


@router.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        response = ServiceLineBot.execute_action(message=event.message.text)

        if not response:
            return

        await line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=response
        )

    return 'OK'
