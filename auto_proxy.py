import asyncio

import aiohttp
from loguru import logger


class ProxyFetcher:
    def __init__(self, proxy_url, proxy_file):
        self.proxy_url = proxy_url
        self.proxy_file = proxy_file

    async def fetch_proxies(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.proxy_url) as response:
                    if response.status == 200:
                        proxies = (await response.text()).strip().splitlines()
                        logger.info(f"Fetched {len(proxies)} proxies from API.")
                        return proxies
                    else:
                        logger.warning(f"Failed to fetch proxies. Status code: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching proxies: {e}")
            return []

    def save_proxies(self, proxies):
        try:
            with open(self.proxy_file, "w") as file:
                file.writelines([proxy + "\n" for proxy in proxies])
            logger.info(f"Saved {len(proxies)} proxies to {self.proxy_file}.")
        except Exception as e:
            logger.error(f"Error saving proxies: {e}")

    async def run(self):
        proxies = await self.fetch_proxies()
        self.save_proxies(proxies)


async def main():
    proxy_fetcher = ProxyFetcher(
        proxy_url="https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text",
        proxy_file="proxy.txt",
    )
    await proxy_fetcher.run()


asyncio.run(main())
