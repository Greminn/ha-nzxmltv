"""Constants for the NZ XMLTV integration."""

from datetime import timedelta

DOMAIN = "nzxmltv"

CONF_PROVIDER = "provider"
CONF_VARIANT = "variant"
CONF_CHANNELS = "channels"

BASE_URL = "https://nzxmltv.com"

# provider -> (display name, base path, {variant: file name})
PROVIDERS: dict[str, tuple[str, str, dict[str, str]]] = {
    "freeview": (
        "Freeview",
        "freeview",
        {
            "static": "guide-static.xml.gz",
            "standard": "guide.xml.gz",
            "lite": "freeview-lite.xml.gz",
        },
    ),
    "sky": (
        "Sky",
        "sky",
        {
            "static": "guide-static.xml.gz",
            "standard": "guide.xml.gz",
            "lite": "sky-lite.xml.gz",
        },
    ),
    "threenow": (
        "ThreeNow",
        "iptv",
        {
            "static": "threenow-static.xml.gz",
            "standard": "threenow.xml.gz",
            "lite": "threenow-lite.xml.gz",
        },
    ),
    "tvnz": (
        "TVNZ+",
        "iptv",
        {
            "static": "tvnz-static.xml.gz",
            "standard": "tvnz.xml.gz",
            "lite": "tvnz-lite.xml.gz",
        },
    ),
}

DEFAULT_VARIANT = "static"
UPDATE_INTERVAL = timedelta(hours=6)


def guide_url(provider: str, variant: str) -> str:
    """Return the guide download URL for a provider/variant."""
    _, path, files = PROVIDERS[provider]
    return f"{BASE_URL}/{path}/{files[variant]}"
