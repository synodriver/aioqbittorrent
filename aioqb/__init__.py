"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
# https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#general-information

from aioqb.client import QbittorrentClient as Client
from aioqb.exceptions import (
    ApiFailedException,
    BaseQbittorrentException,
    HashNotFoundException,
    IPBanedException,
)

__version__ = "0.1.1"
__all__ = [
    "Client",
    "BaseQbittorrentException",
    "IPBanedException",
    "HashNotFoundException",
    "ApiFailedException",
]
