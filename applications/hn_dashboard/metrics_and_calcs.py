from applications.hn_dashboard.sql import get_latest_data_distribution


def get_distribution_of_labels(start, end):
    df = get_latest_data_distribution(start, end)
    dist = df['standard_ml_label'].value_counts()
    return dist
