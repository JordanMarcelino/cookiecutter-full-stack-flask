from typing import Any
from typing import Dict
from urllib.parse import urlparse

import httpx


def post_request(
    url: str, payload: Dict[str, Any], headers: Dict[str, Any] = None
) -> Dict[str, Any]:
    with httpx.Client() as client:
        r = client.post(url=url, json=payload, headers=headers)

        return r.json()


def get_url(base_url: str, endpoint: str):
    parse_url = urlparse(base_url)

    return f"{parse_url.scheme}://{parse_url.hostname}:{parse_url.port}{endpoint}"
