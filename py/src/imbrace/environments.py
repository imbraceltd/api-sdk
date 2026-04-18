from __future__ import annotations
from typing import Literal, Optional
from dataclasses import dataclass, field

Environment = Literal["develop", "sandbox", "stable"]


@dataclass
class ServiceHosts:
    ips: Optional[str] = None
    data_board: Optional[str] = None


@dataclass
class EnvironmentPreset:
    gateway: str
    service_hosts: ServiceHosts = field(default_factory=ServiceHosts)


ENVIRONMENTS: dict[str, EnvironmentPreset] = {
    "develop": EnvironmentPreset(
        gateway="https://app-gateway.dev.imbrace.co",
        service_hosts=ServiceHosts(
            ips="http://ips.dev.imbrace.lan",
            data_board="http://data-board.dev.imbrace.lan",
        ),
    ),
    "sandbox": EnvironmentPreset(
        gateway="https://app-gateway.sandbox.imbrace.co",
    ),
    "stable": EnvironmentPreset(
        gateway="https://app-gateway.imbrace.co",
    ),
}
