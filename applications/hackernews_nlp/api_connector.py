from hackernews import HackerNews
import asyncio


def get_latest_news():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    hn = HackerNews()
    items = hn.new_stories(False, 500)
    return items
