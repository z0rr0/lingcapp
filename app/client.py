from logging import Logger
from typing import Optional
from urllib.parse import urljoin

import httpx


class Client:
    """Lingvo Live API client."""
    SERVICE_URL = 'https://developers.lingvolive.com/'
    USER_AGENT = 'LingCApp/0.1'

    def __init__(self, key: str, timeout: float, logger: Logger) -> None:
        self.key = key
        self.token: Optional[str] = None

        self.timeout = timeout
        self.logger = logger

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
