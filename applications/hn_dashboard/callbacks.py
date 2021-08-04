from applications.hn_dashboard.dashapp import dashApp
from dash.dependencies import Input, Output
from applications.hn_dashboard.metrics_and_calcs import get_distribution_of_labels, get_wordcloud, create_manually_confusion_matrix_for_plotly
import plotly.express as px
from applications.hn_dashboard.sql import calculate_accuracy, get_data_for_confusion_matrix
import plotly.figure_factory as ff


@dashApp.callback(
    Output(component_id='distribution', component_property='figure'),
    Input('date_range', 'start_date'),
    Input('date_range', 'end_date'))
def update_distributions(start, end):
    distribution = get_distribution_of_labels(start, end)
    fig = px.bar(distribution, x=distribution.index, y=distribution, color=distribution.index)
    fig.update_layout(plot_bgcolor='black')
    fig.update_layout(title = f'Total per label for {start[:10]} - {end[:10]}', paper_bgcolor='black', title_font_color="skyblue")
    fig.update_xaxes(title='Label', color="skyblue", showgrid=False)
    fig.update_yaxes(title='Count', color="skyblue", showgrid=False)
    return fig


@dashApp.callback(
    Output(component_id='wordcloud', component_property='figure'),
    Input('dropdown_words', 'value')
)
def update_dropdown(val):
    pic = get_wordcloud(val)
    fig = px.imshow(pic)
    fig.update_layout(plot_bgcolor='black')
    fig.update_layout(title=f'Most frequent words in {val}', paper_bgcolor='black',
                      title_font_color="skyblue")
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    return fig


@dashApp.callback(
    Output(component_id='time_series_accuracy', component_property='figure'),
    Input('dropdown_words', 'value')
)
def update_accuracy(hidden_trigger):
    data = calculate_accuracy()
    fig = px.line(data, x=data['date'], y=data['accuracy'], hover_data=["date", "accuracy"])
    fig.update_layout(plot_bgcolor='black', showlegend=False)
    fig.update_layout(title=f'Accuracy across time(manual check)', paper_bgcolor='black',
                      title_font_color="skyblue")
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(showgrid=False,  color="skyblue")
    fig.update_yaxes(title='Accuracy %', color="skyblue", showgrid=False)
    return fig


@dashApp.callback(
    Output(component_id='confusion_matrix', component_property='figure'),
    Input('dropdown_words', 'value')
)
def update_heatmap_with_accuracy(hidden_trigger):
    data = get_data_for_confusion_matrix()
    data = create_manually_confusion_matrix_for_plotly(data)
    x = list(data.keys())
    fig = ff.create_annotated_heatmap(list(data.values()), x=x, y=x, colorscale='Purples', hoverinfo='x')
    fig.update_layout(plot_bgcolor='black', showlegend=False)
    fig.update_layout( paper_bgcolor='black',
                      title_font_color="skyblue")
    fig.update_xaxes(title='Predicted Label',showgrid=False,  color="skyblue")
    fig.update_yaxes(title='Correct Label', color="skyblue", showgrid=False)
    return fig


