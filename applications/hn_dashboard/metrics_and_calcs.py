from applications.hn_dashboard.sql import get_latest_data


def calculate_accuracy():
    df = get_latest_data()
    accuracy = round(
        (df[df['standard_ml_label'] == df['actual_label']].shape[0] / df[~df['actual_label'].isnull()].shape[0] * 100),
        2)
    return accuracy
