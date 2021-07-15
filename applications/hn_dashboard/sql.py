from sqlalchemy import create_engine
import pandas as pd
import os


def get_latest_data_distribution(start, end):
    distribution_query = f'''
    SELECT standard_ml_label 
    FROM hn_topic_labelling
    WHERE CAST(date as date) BETWEEN '{start[:10]}' and '{end[:10]}';
    '''

    connection = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(distribution_query, con=connection)
    return df


def get_latest_text(topic):

    words_query = f'''
    SELECT raw_txt 
    FROM hn_topic_labelling
    WHERE standard_ml_label = '{topic}'
    ORDER BY id DESC
    LIMIT 3;
    '''

    connection = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(words_query, con=connection)
    return df


def calculate_accuracy():

    get_correct_answers_by_date = f'''
    
    SELECT date, 
    COUNT(actual_label) FILTER (WHERE actual_label = standard_ml_label) as correct, 
    COUNT(actual_label) FILTER (WHERE actual_label IS NOT NULL) as total_reviewed
    FROM hn_topic_labelling 
    GROUP BY 1
    ORDER BY 1;
    '''

    connection = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(get_correct_answers_by_date, con=connection)
    df['accuracy'] = round((df['correct'] / df['total_reviewed'] * 100), 2)
    return df

