<h1 align="center"><i>✨ aioqb ✨ </i></h1>

<h3 align="center">The asyncio  <a href="https://github.com/qbittorrent/qBittorrent">Qbittorrent Client</a> </h3>



[![pypi](https://img.shields.io/pypi/v/aioqb.svg)](https://pypi.org/project/aioqb/)
![python](https://img.shields.io/pypi/pyversions/aioqb)
![implementation](https://img.shields.io/pypi/implementation/aioqb)
![wheel](https://img.shields.io/pypi/wheel/aioqb)
![license](https://img.shields.io/github/license/synodriver/aioqbittorrent.svg)
![action](https://img.shields.io/github/workflow/status/synodriver/aioqbittorrent/build%20wheel)

# The asyncio Qbittorrent Client

```python
import asyncio
import aioqb


async def main():
    client = aioqb.QbittorrentClient()
    await client.torrents_add(torrents=[open("xxx.torrent", "rb")])
    print(await client.transfer_info())
    print(await client.torrents_info())


asyncio.run(main())
```
### Auto ban thunder

```python
"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
# Auto ban xunlei without qbee
import asyncio
from pprint import pprint
from aioqb import Client

block_list = ["xl", "xunlei"]


async def main():
    async with Client() as client:
        pprint(await client.auth_login())
        while True:
            d = await client.sync_maindata()
            # pprint(d)
            torrent_hashs = d['torrents'].keys()
            rid = d['rid']
            for t in torrent_hashs:
                data = await client.sync_torrentPeers(hash=t, rid=0)
                # filter(lambda x: for ip, peer in data["peers"].items() if , block_list)
                for ip, peer in data["peers"].items():
                    # print(ip)
                    # pprint(v)
                    for b in block_list:
                        if b in peer['client'].lower():
                            await client.transfer_banPeers(ip)
                            print(f"ban peer {ip} {peer['client']}")
                            break
            await asyncio.sleep(1)


asyncio.run(main())

```