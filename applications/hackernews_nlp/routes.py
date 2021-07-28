from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import get_latest_news
from applications.hackernews_nlp.ai_handling.predictors import loaded_models,  clean_text, remove_stopwords, label_news
from db_models.hackerNewsModels import TopicLabel
from app import db
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():
    return render_template('hacker_news.html')


def populate_api():
    items = get_latest_news()
    logistic_regression_predictor = loaded_models
    news_content = [[item.text, item.title, item.url] for item in items if item.text is not None]
    """
    Using preprocessing functions from predictors.py for both Naive Bayes and RNN
    """
    news_txt = [x[0] for x in news_content]
    titles = [x[1] if x else 'No Title' for x in news_content]
    cleaned_text = clean_text(news_txt)
    cleaned_from_stopwords = remove_stopwords(cleaned_text)
    lr_final_labels = label_news(cleaned_from_stopwords, logistic_regression_predictor)
    list_of_dicts = [{'text': news_txt[i],
                      'title': titles[i],
                      'pred': lr_final_labels[i]
                      } for i in range(len(lr_final_labels))] # Object to be displayed in html template

    """
    Adding everything to DB if its new
    """
    for i in range(len(news_txt)):
        q = db.session.query(TopicLabel).filter(TopicLabel.raw_txt == news_txt[i])
        if not db.session.query(q.exists()).scalar():
            topic_label = TopicLabel(raw_txt=news_txt[i],
                                     title=titles[i],
                                     date=datetime.today(),
                                     standard_ml_label=lr_final_labels[i],
                                     )

            db.session.add(topic_label)
            db.session.commit()
    print(f'Scheduler execution successful at {datetime.now()}')


scheduler = BackgroundScheduler()
scheduler.add_job(func=populate_api, trigger='interval', seconds=60)
scheduler.start()
