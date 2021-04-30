from hackernews import HackerNews


hn = HackerNews()
DESIRED_ITEM_TYPES = ['comment', 'story', 'job']
hn_obj = ''
comment_about = ''

items = hn.get_last(100)

for item in items:
    if item.text and item.item_type in DESIRED_ITEM_TYPES:
        hn_obj = item
        if item.item_type == 'comment':
            parent_id = item.parent
            comment_about = hn.get_item(parent_id)
        break
