from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import get_latest_news
from applications.hackernews_nlp.ai_handling.predictors import loaded_models, text_to_sequence, get_labels, clean_text, remove_stopwords, label_news
from db_models.hackerNewsModels import TopicLabel
from app import db
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():

    """
    Loading HackerNews items objects on refresh
    """
    items = get_latest_news()
    naive_bayes_predictor, gru_predictor, tokenizer = loaded_models
    news_content = [[item.text, item.title] for item in items if item.text is not None]
    """
    Using preprocessing functions from predictors.py for both Naive Bayes and RNN
    """
    news_txt = [x[0] for x in news_content]
    titles = [x[1] if x else 'No Title' for x in news_content]
    cleaned_text = clean_text(news_txt)
    cleaned_from_stopwords = remove_stopwords(cleaned_text)
    nb_final_labels = label_news(cleaned_from_stopwords, naive_bayes_predictor)
    tokenized_text = text_to_sequence(cleaned_text, tokenizer)
    nn_predictions = gru_predictor.predict(tokenized_text)
    nn_predictions = get_labels(nn_predictions)
    list_of_dicts = [{'text': news_txt[i],
                      'title': titles[i],
                      'pred': nb_final_labels[i],
                      'nn_preds': nn_predictions[i]
                      } for i in range(len(nb_final_labels))] # Object to be displayed in html template

    """
    Adding everything to DB if its new
    """
    for i in range(len(news_txt)):
        q = db.session.query(TopicLabel).filter(TopicLabel.raw_txt == news_txt[i])
        if not db.session.query(q.exists()).scalar():
            topic_label = TopicLabel(raw_txt=news_txt[i],
                                     title=titles[i],
                                     date=datetime.today(),
                                     standard_ml_label=nb_final_labels[i],
                                     neural_net_label=nn_predictions[i]
                                     )

            db.session.add(topic_label)
            db.session.commit()
    try:
        return render_template('news_topics_labels.html', object=list_of_dicts)
    except Exception as e:
        print(f'Scheduler execution successful at {datetime.now()}')


scheduler = BackgroundScheduler()
scheduler.add_job(func=news_labels_page, trigger='interval', seconds=60)
scheduler.start()
