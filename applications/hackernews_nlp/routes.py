from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import get_latest_news
from applications.hackernews_nlp.ai_handling.predictors import loaded_models, text_to_sequence, get_labels, clean_text, remove_stopwords, label_news
from db_models.hackerNewsModels import TopicLabel
from app import db

news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():
    """
    Loading HackerNews items objects on refresh
    """
    items = get_latest_news()
    naive_bayes_predictor, gru_predictor, tokenizer = loaded_models
    news_content = [item.text for item in items if item.text != None]
    """
    Using preprocessing functions from predictors.py for both Naive Bayes and RNN
    """
    cleaned_text = clean_text(news_content)
    cleaned_from_stopwords = remove_stopwords(cleaned_text)
    nb_final_labels = label_news(cleaned_from_stopwords, naive_bayes_predictor)
    # tokenized_text = text_to_sequence(cleaned_text, tokenizer)
    # nn_predictions = gru_predictor.predict(tokenized_text)
    # nn_predictions = get_labels(nn_predictions)
    list_of_dicts = [{'text': news_content[i],
                      'pred': nb_final_labels[i],
                      # 'nn_preds': nn_predictions[i]
                      } for i in range(len(nb_final_labels))] # Object to be displayed in html template

    """
    Adding everything to DB if its new
    """
    for i in range(len(news_content)):
        q = db.session.query(TopicLabel).filter(TopicLabel.raw_txt == news_content[i])
        if not db.session.query(q.exists()).scalar():
            topic_label = TopicLabel(raw_txt=news_content[i],
                                     standard_ml_label=nb_final_labels[i],
                                     # neural_net_label=nn_predictions[i]
                                     )

            db.session.add(topic_label)
            db.session.commit()

    return render_template('news_topics_labels.html', object=list_of_dicts)
