from applications.hn_dashboard.dashapp import dashApp
from dash.dependencies import Input, Output
from applications.hn_dashboard.metrics_and_calcs import get_distribution_of_labels, get_wordcloud
import plotly.express as px
from plotly.subplots import make_subplots


@dashApp.callback(
    Output(component_id='distribution', component_property='figure'),
    Input('date_range', 'start_date'),
    Input('date_range', 'end_date'))
def update_distributions(start, end):
    distribution = get_distribution_of_labels(start, end)
    fig = px.bar(distribution, x=distribution.index, y=distribution, color=distribution.index, color_discrete_map={
        'general': 'purple',
        'web/mobile': 'skyblue',
        'finance': 'orange',
        'devops/OS': 'darkblue',
        'job/career': 'darkred',
        'AI/Data Science': 'white'
    })
    fig.update_layout(width=700, height=650, plot_bgcolor='black')
    fig.update_layout(title = f'Total per label for {start[:10]} - {end[:10]}', paper_bgcolor='black', title_font_color="skyblue")
    fig.update_xaxes(title='Label', color="skyblue")
    fig.update_yaxes(title='Count', color="skyblue")
    return fig


@dashApp.callback(
    Output(component_id='wordcloud', component_property='figure'),
    Input('dropdown_words', 'value')
)
def update_dropdown(val):
    pic = get_wordcloud(val)
    fig = px.imshow(pic)
    fig.update_layout(width=700, height=650, plot_bgcolor='black')
    fig.update_layout(title=f'Most frequent words in {val}', paper_bgcolor='black',
                      title_font_color="skyblue")
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    return fig