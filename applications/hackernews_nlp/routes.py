from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import hn_obj

news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():
    item_to_render = hn_obj
    return render_template('news_topics_labels.html', item=item_to_render)
