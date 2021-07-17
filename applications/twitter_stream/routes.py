from flask import render_template, Blueprint, request
from applications.twitter_stream.api_connector import api as ap

twitter_stream = Blueprint('twitter_stream', __name__, template_folder='templates')


@twitter_stream.route('/twitter_stream/', methods=['GET', 'POST'])
def news_labels_page():
    if request.method == 'POST':
        keyword = request.form['text']
        searched_tweets = ap.search(q=keyword, lang='en', count=20, tweet_mode='extended')
        tweets = [searched_tweets[i]._json['full_text'] for i in range(len(searched_tweets))]
        return render_template('twitter_stream.html', tweets=tweets)
    return render_template('twitter_stream.html')

