from hackernews import HackerNews

hn = HackerNews()
hn_obj = ''

items = hn.new_stories(False, 500)


for item in items:
    if item.text and item.item_type == 'story':
        hn_obj = item
        break

