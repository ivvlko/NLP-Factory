from hackernews import HackerNews
import threading
import asyncio


def get_latest_news():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hn = HackerNews()
    threading.Timer(30, get_latest_news).start()
    items = hn.new_stories(False, 500)
    return items
