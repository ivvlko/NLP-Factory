from hackernews import HackerNews
import asyncio

hn = HackerNews()


def get_latest_news(hn_obj=hn):
    """
    Extracts latest news
    :param hn_obj: global HackerNews object
    :return: list of strings
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    items = hn_obj.new_stories(False, 500)
    return items
