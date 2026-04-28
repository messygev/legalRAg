from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class RisConfig:
    base_url: str = "https://testphase.rechtsinformationen.bund.de"
    timeout_seconds: float = 30.0
    page_size: int = 100


class RisApiError(RuntimeError):
    pass


class RisApiConnector:
    def __init__(self, config: RisConfig | None = None):
        self.config = config or RisConfig()
        self.client = httpx.Client(base_url=self.config.base_url, timeout=self.config.timeout_seconds, headers={"Accept": "application/json"})

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.client.get(path, params=params)
        if response.status_code >= 400:
            raise RisApiError(f"RIS API error {response.status_code}: {response.text[:500]}")
        return response.json()

    def _get_raw(self, path_or_url: str) -> bytes:
        response = self.client.get(path_or_url, headers={"Accept": "*/*"})
        if response.status_code >= 400:
            raise RisApiError(f"RIS API raw error {response.status_code}: {response.text[:500]}")
        return response.content

    def statistics(self) -> dict[str, Any]:
        return self._get_json("/v1/statistics")

    def search_legislation(self, search_term: str | None = None, effective_date: str | None = None, page_index: int = 0, size: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"pageIndex": page_index, "size": size or self.config.page_size}
        if search_term:
            params["searchTerm"] = search_term
        if effective_date:
            params["temporalCoverageFrom"] = effective_date
            params["temporalCoverageTo"] = effective_date
        return self._get_json("/v1/legislation", params=params)

    def fetch_encoding(self, content_url: str) -> bytes:
        return self._get_raw(content_url)

    @staticmethod
    def sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
