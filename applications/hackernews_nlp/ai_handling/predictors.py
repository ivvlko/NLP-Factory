import re
import nltk
import pickle
nltk.download('stopwords')
from nltk.corpus import stopwords

# Constants
MAX_NUM_WORDS = 400
MAPPING_DICT = {0: 'AI/Data Science', 1: 'devops/OS', 2: 'finance', 3: 'general', 4: 'job/career',
                5: 'web/mobile'}

lr_path = 'applications/hackernews_nlp/ai_handling/ai_models/lr.pickle'


def load_models(path):
    opener = open(path, 'rb')
    nb = pickle.load(opener)
    opener.close()
    return nb


loaded_models = load_models(lr_path)


def get_labels(preds):
    final_labels = []
    for arr in preds:
        find_max = arr.max()
        find_index = arr.tolist().index(find_max)
        final_labels.append(MAPPING_DICT[find_index])
    return final_labels


def clean_text(series):
    cleaned_txt = []
    for text in series:
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
        text = re.sub(r'quot', '', text)
        text = re.sub(r'x27', '', text)
        text = text.strip(' ')
        cleaned_txt.append(text)
    return cleaned_txt


def remove_stopwords(series):
    removed_stopwords_series = []
    for row in series:
        final_row = [w for w in row.split(' ') if w not in stopwords.words('english')]
        final_row = ' '.join(final_row)
        removed_stopwords_series.append(final_row)
    return removed_stopwords_series


def label_news(processed_text, model):
    labels = model.predict(processed_text)
    labels = [MAPPING_DICT[label] for label in labels]
    return labels

