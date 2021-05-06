from flask import render_template, Blueprint
from applications.hackernews_nlp.api_connector import get_latest_news
from applications.hackernews_nlp.ai_handling.predictors import StandardMLPredictor, loaded_models, text_to_sequence, get_labels
from db_models.hackerNewsModels import TopicLabel
from app import db

news_topics_labelling = Blueprint('hackernews_nlp', __name__, template_folder='templates')


@news_topics_labelling.route('/news_labels/')
def news_labels_page():
    """
    Loading HackerNews items objects and ML models on refresh
    """
    items = get_latest_news()
    naive_bayes_predictor, gru_predictor, tokenizer = loaded_models
    news_content = [item.text for item in items if item.text != None][:6]
    """
    Using predictors class' methods and static functions to clean, preprocess and label the news
    """
    naive_bayes_predictor = StandardMLPredictor(naive_bayes_predictor)
    cleaned_text = naive_bayes_predictor.clean_text(news_content)
    cleaned_from_stopwords = naive_bayes_predictor.remove_stopwords(cleaned_text)
    nb_final_labels = naive_bayes_predictor.label_news(cleaned_from_stopwords)
    tokenized_text = text_to_sequence(cleaned_text, tokenizer)
    nn_predictions = gru_predictor.predict(tokenized_text)
    nn_predictions = get_labels(nn_predictions)
    list_of_dicts = [{'text': news_content[i],
                      'pred': nb_final_labels[i],
                      'nn_preds': nn_predictions[i]} for i in range(len(nb_final_labels))]
    # Object to be displayed in html template

    """
    Adding everything to DB if its new
    """
    last_6 = db.session.query(TopicLabel.raw_txt).order_by(TopicLabel.id.desc()).limit(6).all()
    last_6 = [x[0] for x in last_6]
    for i in range(len(news_content)):
        if news_content[i] not in last_6:
            topic_label = TopicLabel(raw_txt=news_content[i],
                                     standard_ml_label=nb_final_labels[i],
                                     neural_net_label=nn_predictions[i])

            db.session.add(topic_label)
            db.session.commit()

    return render_template('news_topics_labels.html', object=list_of_dicts)
