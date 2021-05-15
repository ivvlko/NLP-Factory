from applications.hn_dashboard.dashapp import dashApp
from dash.dependencies import Input, Output
from applications.hn_dashboard.metrics_and_calcs import get_distribution_of_labels
import plotly.express as px


@dashApp.callback(
    Output(component_id='distribution', component_property='figure'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date')])
def update_distributions(start, end):
    distribution = get_distribution_of_labels(start, end)
    fig = px.bar(distribution, x=distribution.index, y=distribution, color=distribution.index)
    fig.update_layout(width=600, height=450, plot_bgcolor='black')
    fig.update_layout(title = f'Total per label for {start[:10]} - {end[:10]}', paper_bgcolor='black', title_font_color="crimson")
    fig.update_xaxes(title='Label', color="crimson")
    fig.update_yaxes(title='Count', color="crimson")
    return fig


