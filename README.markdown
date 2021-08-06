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