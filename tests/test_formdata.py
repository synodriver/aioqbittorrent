"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as sessioin:
        data = aiohttp.FormData()
        data.add_field("test", True)


asyncio.run(main())
