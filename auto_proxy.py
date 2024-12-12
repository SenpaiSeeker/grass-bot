import asyncio

import aiohttp
from loguru import logger


class ProxyFetcher:
    def __init__(self, proxy_urls, proxy_file):
        self.proxy_urls = proxy_urls
        self.proxy_file = proxy_file

    async def fetch_proxies(self):
        async with aiohttp.ClientSession() as session:
            proxies = [proxy for url in self.proxy_urls for proxy in await self._fetch_from_url(session, url)]
        return proxies

    async def _fetch_from_url(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    proxies = (await response.text()).strip().splitlines()
                    logger.info(f"Fetched {len(proxies)} proxies from {url}")
                    return proxies
                else:
                    logger.warning(f"Failed to fetch from {url} - Status: {response.status}")
        except Exception as e:
            logger.error(f"Error fetching from {url}: {e}")
        return []

    def save_proxies(self, proxies):
        try:
            with open(self.proxy_file, "w") as file:
                file.writelines([f"http://{proxy}\n" for proxy in proxies])
            logger.info(f"Saved {len(proxies)} proxies to {self.proxy_file}")
        except Exception as e:
            logger.error(f"Error saving proxies: {e}")

    async def run(self):
        proxies = await self.fetch_proxies()
        self.save_proxies(proxies)


async def main():
    proxy_fetcher = ProxyFetcher(
        proxy_urls=[
            #"https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
            "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS_RAW.txt"
        ],
        proxy_file="proxy.txt",
    )
    await proxy_fetcher.run()


if __name__ == "__main__":
    asyncio.run(main())
