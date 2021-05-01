import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pickle


def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\d', '', text)
    text = text.strip(' ')
    return text


def remove_stopwords(row):
    final_row = [w for w in row.split(' ') if w not in stopwords.words('english')]
    final_row = ' '.join(final_row)
    return final_row


def label_news(processed_text):
    mapping_dict = {0: 'automobile', 1: 'science', 2: 'politics',3: 'technology', 4: 'sports', 5: 'entertainment', 6: 'world'}
    opener = open('applications/hackernews_nlp/ai_handling/nb_topic_classifier.pickle', 'rb')
    model = pickle.load(opener)
    opener.close()
    labels = model.predict(processed_text)
    labels = [mapping_dict[label] for label in labels]
    return labels
