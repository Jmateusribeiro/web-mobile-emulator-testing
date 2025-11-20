"""
Mobile device profiles for browser emulation.

This module contains predefined mobile device configurations that can be used
for browser mobile emulation testing.
"""
from typing import Dict, NamedTuple


class DeviceProfile(NamedTuple):
    """
    Mobile device profile configuration.

    Attributes:
        name (str): Device name/identifier.
        width (int): Screen width in pixels.
        height (int): Screen height in pixels.
        pixel_ratio (float): Device pixel ratio (DPR).
        user_agent (str): User agent string for the device.
    """
    name: str
    width: int
    height: int
    pixel_ratio: float
    user_agent: str


# iOS Devices
IPHONE_8 = DeviceProfile(
    name="iPhone 8",
    width=375,
    height=667,
    pixel_ratio=2.0,
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)


# Android Devices
PIXEL_7 = DeviceProfile(
    name="Pixel 7",
    width=412,
    height=915,
    pixel_ratio=2.625,
    user_agent="Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
)


# Default device for testing
DEFAULT_DEVICE = IPHONE_8


def to_mobile_emulation(device: DeviceProfile) -> Dict:
    """
    Convert device profile to mobile emulation configuration dictionary.

    Args:
        device (DeviceProfile): Device profile to convert.

    Returns:
        Dict: Mobile emulation configuration compatible with Chrome/Edge.

    Example:
        >>> emulation = to_mobile_emulation(IPHONE_8)
        >>> chrome_options.add_experimental_option("mobileEmulation", emulation)
    """
    return {
        "deviceMetrics": {
            "width": device.width,
            "height": device.height,
            "pixelRatio": device.pixel_ratio
        },
        "userAgent": device.user_agent
    }