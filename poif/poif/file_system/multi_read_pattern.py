import asyncio
from collections import defaultdict
import aiohttp

http_retrievals = {}
retrieval_locks = {}
reader_count = defaultdict(list)

add_new_retrieval_lock = asyncio.Lock()
decrease_reader_lock = asyncio.Lock()

data_buffer = {}


async def get_url_bytes(url, offset, length):
    first_reader = False
    async with add_new_retrieval_lock:
        reader_count[url] += 1
        if reader_count[url] == 1:
            # You are the first reader
            first_reader = True
            retrieval_locks[url] = asyncio.Event()
    if first_reader:
        retrieve_url(url)
    await retrieval_locks[url]

    async with decrease_reader_lock:
        data = data_buffer[url][offset: offset + length]
        reader_count[url] -= 1
        if reader_count[url] == 0:
            data_buffer[url] = None
    return data


async def retrieve_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data_buffer[url] = response.content



