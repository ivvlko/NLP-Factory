import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import datetime
import datetime as dt

layout = html.Div(children=[
    dbc.Row(id='heading', children=[
        dbc.Col(html.A('Home', id='go_back_home', href='/'), width=2),
        dbc.Col(html.H1(f'HackerNews App Summary Dashboard', className='heading-h'), width=10, style={'margin-left': '-120px'})
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='wrapper', children=[

                html.Div(id='distribution_container', children=[
                    html.Label(id='range-label', htmlFor='date_range', children=[html.H3('Date Range:  ')]),
                    dcc.DatePickerRange(
                        id='date_range',
                        start_date=datetime.today() - dt.timedelta(days=3),
                        end_date=datetime.today(),
                    ),

                    dcc.Loading(dcc.Graph(id='distribution')),
                ]),
            ])
        ], width=6),
        dbc.Col([
            html.Div(id='wordscloud_container', children=[
                html.Label(htmlFor='dropdown_words', children=[html.H3('Label: ')], style={'display': 'flex'}),
                dcc.Dropdown(id='dropdown_words',
                             options=[{'label': 'web/mobile', 'value': 'web/mobile'},
                                      {'label': 'AI/Data Science', 'value': 'AI/Data Science'},
                                      {'label': 'devops/OS', 'value': 'devops/OS'},
                                      {'label': 'job/career', 'value': 'job/career'},
                                      {'label': 'finance', 'value': 'finance'},
                                      {'label': 'general', 'value': 'general'}],
                             value='web/mobile'
                             ),
                dcc.Loading(dcc.Graph(id='wordcloud'))
            ])], width=6)]),

        dbc.Row(id='time_series_accuracy_container', children=[
            dbc.Col(dcc.Loading(dcc.Graph(id='time_series_accuracy')), width=12),

    ]),

])
