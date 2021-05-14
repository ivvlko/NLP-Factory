import dash_core_components as dcc
import dash_html_components as html
from applications.hn_dashboard.metrics_and_calcs import calculate_accuracy


layout = html.Div(children=[

    html.H1(f'All Time Accuracy: Naive Bayes(manually checked) : {calculate_accuracy()}'),

])


