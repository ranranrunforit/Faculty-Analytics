from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
from academic_world_project.dbs.neo4j_utils import get_institutes, get_faculties, get_faculty_data


def generate_view_faculty(app: Dash) -> list:
    @app.callback(
        Output("faculty", "options"),
        Input("universities", "value")
    )
    def faculty_selection(university_input):
        faculties_from_db = get_faculties(university_input)
        return faculties_from_db

    @app.callback(
        Output('view_member', 'children'),
        Input('faculty', 'value')
    )
    def display_faculty_data(faculty_name):
        faculty_data, keywords = get_faculty_data(faculty_name)
        result0 = "Top 5 keywords interested in : "
        if keywords is not None:
            result = ", ".join(keywords)
        else:
            result = ""
        first_card = dbc.Card(
            dbc.CardBody(
                [
                    dbc.CardImg(src=faculty_data['photoUrl'], top=True),
                    #dbc.CardBody(
                    html.H4(faculty_name, className="card-title"),
                    html.H6(faculty_data['position'], className="card-subtitle"),
                    # html.P(faculty_data['institute_name'], className="card-text")
                  #  ),
                ], style={"width": "15rem"}, # style={"max-width: 20rem"},
            )
        )
        
        
        second_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Contact Infomation", className="card-title"),
                    html.P(
                       dbc.Table([html.Thead(
                           html.Tr([
                               html.Th('Faculty Fields',style={'textAlign': 'center'}),
                               html.Th('Faculty Values',style={'textAlign': 'center'})
                          ])),
                          html.Tbody([html.Tr([
                               html.Td('Phone',style={'textAlign': 'center'}),
                               html.Td(faculty_data['phone'],style={'textAlign': 'center'})
                           ]),
                           html.Tr([
                               html.Td('Email',style={'textAlign': 'center'}),
                               html.Td(faculty_data['email'],style={'textAlign': 'center'})
                           ]),
                           html.Tr([
                               html.Td('Position',style={'textAlign': 'center'}),
                               html.Td(faculty_data['position'],style={'textAlign': 'center'})
                           ]),
                           html.Tr([
                               html.Td('Institute Name',style={'textAlign': 'center'}),
                               html.Td(faculty_data['institute_name'],style={'textAlign': 'center'})
                           ])
                       ]) #className="p-3 m-2 border",
                       ],color="secondary",bordered=True,hover=True,responsive=True, size='lg',#style={"width": "65%"}
                       ),
                    ),
                    
                    html.H6(result0, className="card-subtitle"),
                    html.P(result, className="card-text")
                    
                ], #style={"width": "18rem"},
            )
        )
        
        
        cards = dbc.Row(
            [
                dbc.Col(first_card, width=4),
                dbc.Col(second_card, width=8),
            ]
        )
        return  cards

    institutes_from_db = get_institutes()
    return [
        #html.Br(),
        html.Div(
           children=[
               html.H1('Find the Faculty Data',style={'textAlign': 'center','margin': '0 auto'}),
        #html.Br(),
        # faculty add, delete, modify keywords widget
        #html.H2(children='Select the University',style={'textAlign': 'center'}),
        ],#222222 #e9e9e8 #686dc3
        className="header", style={'height': '168px','padding': '16px 0 0 0'}
    ),
        html.Div(
           children=[
        html.Div(
            children=[
                html.Div(children='Institute', className="menu-title", style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#39cbfb'}),# #079A82
                dcc.Dropdown(
            id='universities',
            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'400px'},# DeepSkyBlue # #39cbfb
            options=institutes_from_db,
            value='University of California--Berkeley',
            clearable=False,
        ),
        #style=dict(display='flex', justifyContent='center')
        ]
    ),
        #html.H2(children='Select the Faculty ',style={'textAlign': 'center'}),
        html.Div(
            children=[
                html.Div(children='Faculty', className="menu-title", style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#39cbfb'}),# #079A82
                dcc.Dropdown(
            id='faculty',
            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'400px'},
            value='Sarah Chasins',
            clearable=False,
        ),
        #style=dict(display='flex', justifyContent='center')
        ]
    ),
        
        ],
        className="menu", style={  'height': '112px','width': '912px','display': 'flex', 'justify-content': 'space-evenly', 'padding-top': '24px', 'margin': '-80px auto 0 auto','background-color': '#FFFFFF', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'}
    ),
        html.Br(),
        #html.H2(children='Faculty Data',style={'textAlign': 'center'}),
        html.H2(children='Faculty Information',style={'textAlign': 'center'}),
        html.Div(id='view_member', children='',
        className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
        ),
        html.Br()
    ]
