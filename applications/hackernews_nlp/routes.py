from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import items
from applications.hackernews_nlp.ai_handling.handler import clean_text, remove_stopwords, label_news
news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():
    print(items)
    news_content = [item.text for item in items if item.text != None]
    cleaned_text = [clean_text(txt) for txt in news_content]
    cleaned_text = [remove_stopwords(txt) for txt in cleaned_text]
    final_labels = label_news(cleaned_text)
    list_of_dicts = [{'text': news_content[i], 'pred': final_labels[i]} for i in range(len(final_labels))]
    return render_template('news_topics_labels.html', object=list_of_dicts)
