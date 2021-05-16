from sqlalchemy import create_engine
import pandas as pd
import os


def get_latest_data_distribution(start, end):
    distribution_query = f'''
    SELECT standard_ml_label 
    FROM hn_topic_labelling
    WHERE CAST(date as date) BETWEEN '{start[:10]}' and '{end[:10]}';
    '''

    conn = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(distribution_query, con=conn)
    return df


def get_latest_text(topic):

    words_query = f'''
    SELECT raw_txt 
    FROM hn_topic_labelling
    WHERE standard_ml_label = '{topic}'
    ORDER BY date DESC
    LIMIT 50;
    '''

    conn = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(words_query, con=conn)
    return df
