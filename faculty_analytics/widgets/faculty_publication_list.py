from academic_world_project.dbs.mysql_utils import MYSQL

from dash import dcc, html, Dash, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


def get_publications_by_faculty(app: Dash) -> list:
    @app.callback(Output('publication-form2', 'figure'),
                  Input('submit-button-faculty', 'n_clicks'),
                  State('my-faculty', 'value'))
    def update_output(n_clicks, faculty):
        return get_faculty_publication_list(faculty)

    return [
        html.H1(children='Find Publication by faculty',style={'textAlign': 'center'}),
        html.Div(
            children=[ dbc.Input(id='my-faculty', value='Fei Wang',placeholder="Type the faculty name here...", type='text',style={"width": 800, "height": 50, 'textAlign': 'center'}),    
                      dbc.Button(id='submit-button-faculty', n_clicks=0, children='Search', color="secondary",size="lg", className="me-1"),
        ],style=dict(display='flex', justifyContent='center')
     ),
        html.Div(children=[
               html.Div( children =dcc.Graph(id='publication-form2',config={"displayModeBar": False}, ),
           className="card", style = {'margin-bottom': '24px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',},
           )
       ],
        className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
    ),
            ]   


def get_faculty_publication_list(faculty) -> go.Figure:
    mysql = MYSQL()
    df = mysql.get_publication_by_faculty(faculty, 0)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    align='left'),
        cells=dict(values=[df.publication_id, df.publication_name, df.year, df.num_of_citations, df.professor],
                   align='left'))
    ])

    return fig
