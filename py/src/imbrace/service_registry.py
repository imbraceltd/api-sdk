from __future__ import annotations
from typing import Optional, Union, Dict
from dataclasses import dataclass

from .environments import EnvironmentPreset, ENVIRONMENTS


@dataclass
class ServiceUrls:
    gateway: str
    channel_service: str
    platform: str
    ips: str
    data_board: str
    backend: str
    ai: str
    marketplaces: str
    file_service: str
    message_suggestion: str
    predict: str
    activepieces: str


def resolve_service_urls(
    env: Union[str, EnvironmentPreset],
    overrides: Optional[Dict[str, str]] = None,
) -> ServiceUrls:
    if isinstance(env, str):
        preset = ENVIRONMENTS[env]
    else:
        preset = env

    gw = preset.gateway.rstrip("/")

    is_v2 = env == "prodv2" or "app-gatewayv2" in gw

    resolved = ServiceUrls(
        gateway=gw,
        channel_service=f"{gw}/channel-service",
        platform=f"{gw}/platform",
        ips=f"{(preset.service_hosts.ips or gw).rstrip('/')}/ips/v1",
        data_board=f"{gw}/data-board",
        backend=f"{gw}/v2/backend" if is_v2 else f"{gw}/v1/backend",
        ai=gw,
        marketplaces=f"{gw}/v2/backend/marketplaces",
        file_service=f"{gw}/v2/backend/file-service" if is_v2 else f"{gw}/v1/backend/file-service",
        message_suggestion=f"{gw}/v1/message-suggestion",
        predict=f"{gw}/predict",
        activepieces=f"{gw}/activepieces",
    )

    if overrides:
        for key, value in overrides.items():
            if hasattr(resolved, key) and value is not None:
                setattr(resolved, key, value)

    return resolved
