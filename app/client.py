import time
from logging import Logger
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from .items import MiniCard


class Client:
    """Lingvo Live API client."""
    SERVICE_URL = 'https://developers.lingvolive.com/'
    USER_AGENT = 'LingCApp/0.1'

    def __init__(self, key: str, timeout: float, logger: Logger, verbose: bool = False) -> None:
        self.key = key
        self.token: Optional[str] = None

        self.timeout = timeout
        self.logger = logger
        self.verbose = verbose

    @staticmethod
    def duration_ms_from(start: int) -> float:
        """
        It returns the duration in milliseconds.
        Where start is the time.monotonic_ns() value.
        """
        return (time.monotonic_ns() - start) / 1_000_000

    @property
    def base_headers(self) -> dict[str, str]:
        return {
            'User-Agent': self.USER_AGENT,
            'Content-Length': '0',
        }

    def url(self, path: str) -> str:
        """Returns full URL for custom request path."""
        return urljoin(self.SERVICE_URL, path)

    def authenticate(self) -> bool:
        url = self.url('api/v1.1/authenticate')
        headers = self.base_headers
        headers.update({'Authorization': f'Basic {self.key}'})

        try:
            response = httpx.post(url, headers=headers, timeout=self.timeout)
        except httpx.RequestError as exc:
            self.logger.error(f'Error: {exc}')
            return False

        if response.status_code != httpx.codes.OK:
            self.logger.error(f'Error: {response.status_code} {response.reason_phrase}')
            return False

        self.token = response.text.strip('"')
        return True

    async def _common_translate(self, client: httpx.AsyncClient, url: str, params: dict[str, Any]) -> Optional[dict]:
        headers = self.base_headers
        headers.update({'Authorization': f'Bearer {self.token}'})

        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            self.logger.error(f'Error: {exc}')
            return

        return response.json()

    async def mini_card(self, client: httpx.AsyncClient, text: str, src: int, dst: int) -> Optional[MiniCard]:
        start = time.monotonic_ns()
        url = self.url('api/v1/Minicard')
        params = {'text': text, 'srcLang': src, 'dstLang': dst}

        data = await self._common_translate(client, url, params)
        if not data:
            return

        duration = self.duration_ms_from(start) if self.verbose else 0.0
        return MiniCard(
            heading=data['Heading'],
            translation=data['Translation']['Translation'],
            dictionary=data['Translation']['DictionaryName'],
            duration=duration,
        )

    async def translate(self, client: httpx.AsyncClient, text: str, src: int, dst: int) -> Optional[dict]:
        url = self.url('api/v1/Translation')
        params = {'text': text, 'srcLang': src, 'dstLang': dst}

        return await self._common_translate(client, url, params)
