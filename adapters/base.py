from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class AdapterBase(ABC):
    platform_id: str = ""
    platform_name: str = ""
    adapter_version: str = "0.1.0"

    @abstractmethod
    def install(self, config: dict[str, Any]) -> None:
        """Register hooks and any platform-specific integration."""

    @abstractmethod
    def uninstall(self, config: dict[str, Any]) -> None:
        """Remove all platform-specific integration."""

    @abstractmethod
    def generate_shortcuts(self, config: dict[str, Any]) -> None:
        """Write frequency-ranked shortcut skill files for this platform."""

    @abstractmethod
    def detect_installed(self) -> bool:
        """Return True if this platform is present on the system."""
