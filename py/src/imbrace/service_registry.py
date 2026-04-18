from __future__ import annotations
from typing import Optional, Union
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


def resolve_service_urls(
    env: Union[str, EnvironmentPreset],
    overrides: Optional[dict] = None,
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
    )

    if overrides:
        for key, value in overrides.items():
            if hasattr(resolved, key) and value is not None:
                setattr(resolved, key, value)

    return resolved
