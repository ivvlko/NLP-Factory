import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import datetime as dt

layout = html.Div(children=[

    html.A('Home', id='go_back_home', href='/'),
    html.H1(f'HackerNews App Summary Dashboard', className='heading-h'),

    html.Div(id='distribution_container', children=[
        dcc.DatePickerRange(
            id='date_range',
            start_date=datetime.today() - dt.timedelta(days=7),
            end_date=datetime.today(),
        ),

        dcc.Graph(id='distribution')
    ]),

])
