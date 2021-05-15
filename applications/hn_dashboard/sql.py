from sqlalchemy import create_engine
import pandas as pd
import os


def get_latest_data_distribution(start, end):
    distribution_query = f'''
    SELECT standard_ml_label 
    FROM hn_topic_labelling
    '''

    conn = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(distribution_query, con=conn)
    return df


