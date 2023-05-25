import json
import logging
import os.path
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from .client import Client
from .languages import Language


@dataclass(frozen=True)
class Params:
    """Params aggregator for Handler."""
    key: str
    direction: str
    timeout: float
    src: Language
    dst: Language
    cache_path: str = ''
    verbose: bool = False

    @property
    def cache_file(self) -> Optional[str]:
        if not self.cache_path.endswith('.json'):
            return

        return self.cache_path


class Handler:
    EXPIRED_TTL_FORMAT = '%Y-%m-%d %H:%M:%S'
    TOKEN_TLL = 86340  # token time to live (seconds), 24 hours - 1 minute

    def __init__(self, params: Params) -> None:
        self.key = params.key
        self.direction = params.direction
        self.timeout = params.timeout
        self.cache_file = params.cache_file

        self.src = params.src
        self.dst = params.dst

        self.logger = self.build_logger(params.verbose)
        self.client = Client(self.key, self.timeout, self.logger)

    @staticmethod
    def build_logger(verbose: bool) -> logging.Logger:
        level = logging.DEBUG if verbose else logging.WARNING

        logger = logging.getLogger('lingcapp')
        logger.setLevel(level)

        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        return logger

    def _read_cache(self) -> Optional[str]:
        if not (self.cache_file and os.path.isfile(self.cache_file)):
            return None

        with open(self.cache_file, 'r') as f:
            data = json.load(f)

        if not (data and 'token' in data and 'expired' in data):
            return None

        # data format: {'token': '', 'expired': 'YYYY-MM-DD HH:MM:SS'}, with UTC timezone
        expired = datetime.strptime(data['expired'], self.EXPIRED_TTL_FORMAT)
        now = datetime.utcnow()

        if now > expired:
            return None

        self.logger.debug('read token from file cache')
        return data['token']

    def _write_cache(self) -> None:
        """It writes token to file cache."""
        if not (self.cache_file and self.client.token):
            return

        expired = datetime.utcnow() + timedelta(seconds=self.TOKEN_TLL)
        data = {
            'token': self.client.token,
            'expired': expired.strftime(self.EXPIRED_TTL_FORMAT),
        }
        with open(self.cache_file, 'w') as f:
            json.dump(data, f)

    def auth(self) -> bool:
        """It checks file cache and does authentication request if necessary."""
        if token := self._read_cache():
            self.client.token = token
            return True

        ok = self.client.authenticate()
        self.logger.debug(f'no cache, authenticate: {ok}')

        if ok:
            self._write_cache()
        return ok

    async def run(self, words: list[str]) -> None:
        pass
