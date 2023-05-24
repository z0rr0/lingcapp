import asyncio
import logging
import time

from asyncio.exceptions import TimeoutError
from enum import Enum

import aiohttp

logger = logging.getLogger(__name__)


class Language(Enum):
    # https://developers.lingvolive.com/ru-ru/Dictionaries
    EN = 1033
    RU = 1049

    @classmethod
    def from_str(cls, lang: str) -> 'Language':
        return cls[lang.upper()]


class Client:
    LANG_CHOICES = [
        'auto',
        '{}-{}'.format(Language.EN.name.lower(), Language.RU.name.lower()),
        '{}-{}'.format(Language.RU.name.lower(), Language.EN.name.lower()),
    ]

    def __init__(self, key: str, direction: str, *args: str) -> None:
        self.key = key
        self.args = args
        self.direction = direction

    async def run(self, text: str) -> None:
        pass
