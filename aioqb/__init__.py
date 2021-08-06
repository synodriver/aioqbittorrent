"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
# https://github.com/qbittorrent/qBittorrent/wiki/WebUI-API-(qBittorrent-4.1)#general-information

from aioqb.client import QbittorrentClient
from aioqb.exceptions import (BaseQbittorrentException,
                              IPBanedException,
                              HashNotFoundException,
                              ApiFailedException)

__version__ = "0.1.0"
