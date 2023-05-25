from logging import Logger
from typing import Optional
from urllib.parse import urljoin

import httpx


class Client:
    """Lingvo Live API client."""
    ServiceURL = 'https://developers.lingvolive.com/'
    UserAgent = 'LingCApp/0.1'
    TokenTLL = 86340  # 24 hours - 1 minute

    def __init__(self, key: str, timeout: float, logger: Logger) -> None:
        self.key = key
        self.token: Optional[str] = None

        self.timeout = timeout
        self.logger = logger

    @property
    def headers(self) -> dict[str, str]:
        return {
            'User-Agent': self.UserAgent,
            'Content-Length': '0',
        }

    def authenticate(self) -> bool:
        url = 'api/v1.1/authenticate'
        full_path = urljoin(self.ServiceURL, url)
        headers = self.headers

        headers.update({'Authorization': f'Basic {self.key}'})
        try:
            response = httpx.post(full_path, headers=headers, timeout=self.timeout)
        except httpx.RequestError as exc:
            self.logger.error(f'Error: {exc}')
            return False

        if response.status_code != httpx.codes.OK:
            self.logger.error(f'Error: {response.status_code} {response.reason_phrase}')
            return False

        self.token = response.text.strip('"')
        return True
