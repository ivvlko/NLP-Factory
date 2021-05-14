from sqlalchemy import create_engine
import pandas as pd
import os

query = '''
SELECT * 
FROM hn_topic_labelling
WHERE standard_ml_label IS NOT NULL AND actual_label IS NOT NULL;
'''


def get_latest_data():
    conn = create_engine(
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@localhost:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}")
    df = pd.read_sql_query(query, con=conn)
    return df


