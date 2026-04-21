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

    resolved = ServiceUrls(
        gateway=gw,
        channel_service=f"{gw}/channel-service",
        platform=f"{gw}/platform",
        ips=f"{(preset.service_hosts.ips or gw).rstrip('/')}/ips/v1",
        data_board=f"{(preset.service_hosts.data_board or gw).rstrip('/')}/data-board",
        ai=f"{gw}/ai",
        marketplaces=f"{gw}/marketplaces",
        file_service=f"{gw}/v1/file-service",
        message_suggestion=f"{gw}/v1/message-suggestion",
        predict=f"{gw}/predict",
        activepieces=f"{gw}/activepieces",
    )

    if overrides:
        for key, value in overrides.items():
            if hasattr(resolved, key) and value is not None:
                setattr(resolved, key, value)

    return resolved
