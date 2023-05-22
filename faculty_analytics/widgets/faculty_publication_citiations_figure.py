from dash import dcc, html, Dash, Input, Output
import pandas as pd
from academic_world_project.dbs.neo4j_utils import get_faculty, get_keywords, get_year

from academic_world_project.dbs.mysql_utils import MYSQL

def publication_citiation(app: Dash) -> list:
    @app.callback(
        Output("faculty1", "options"),
        Output('intermediate-value1','data'),
        Input("keyword1", "value")
    )
    
    def faculty_selection1(keyword1_input):
        #faculty_from_db = get_faculty()
        faculty_from_db= get_faculty(keyword1_input)
        return faculty_from_db, keyword1_input

    @app.callback(
        Output("date-range1", "options"),
        Output("date-range2", "options"),
        Output('intermediate-value2','data'),
        Input("faculty1", "value"),
        Input('intermediate-value1','data'),
        
    )
    def year_selection1(faculty1_input, keyword1_input):
        #mysql = MYSQL()
        #year_from_mysql1,year_from_mysql2 = mysql.get_year_by_faculty(keyword1_input,faculty1_input)
        year_from_neo4j1, year_from_neo4j2 = get_year(keyword1_input,faculty1_input)
        
        return  year_from_neo4j1, year_from_neo4j2,faculty1_input

    @app.callback(
        Output("citiations-chart", "figure"),
        Input("date-range1", "value"),
        Input("date-range2", "value"),
        Input('intermediate-value2','data'),
        Input('intermediate-value1','data'),
    )
    
    def generate_citiation_char(date1, date2, faculty1_intput,keyword1_intput):
        mysql = MYSQL()
        result = mysql.get_publication_by_faculty_keyword1( faculty1_intput,keyword1_intput, 0, date1, date2)
        df = pd.DataFrame(result, columns=['num_of_citiations','year','professor_name','keyword_name'], dtype=str)
        
       
        fig = {
            "data": [
                {
                    "x": df["year"],
                    "y": df["num_of_citiations"],
                    "type": "lines",
                    "hovertemplate": "%{y} citations<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": f"Number of Citiations for the Publication with {keyword1_intput} by {faculty1_intput} From {date1} to {date2}",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#41d7a7"],# #17B897
            },
        }


        return fig
   

    keywords_from_db = get_keywords()
    #faculty_from_db = get_faculty()
    #year_from_db = get_year()
    return [
        #html.H1(children='Number of Citations for a Specific Keyword for a Faculty',style={"fontSize": "48px", "color": "red"},),
        html.Div(
           children=[
               html.P(children="🏫", className="header-emoji", style={'font-size': '48px','margin': '0 auto','text-align': 'center'}),
               html.H1(#212529
                   children="Faculty Analytics", className="header-title", style={'color': '#FFFFFF','font-size': '48px', 'font-weight': 'bold','text-align': 'center','margin': '0 auto'}
               ),
               html.P(
                   children=(
                       "Analyze the keyword and the publication that Faculty"
                       " interested in the US Colleges between 1903 and 2021"
                   ), #e9e9e8 #CFCFCF #6c757d
                   className="header-description", style={'color': 'rgba(255, 255, 255, 0.7)','margin': '4px auto','text-align': 'center','max-width': '384px'}
               ),
           ],#222222 #e9e9e8 #686dc3
           className="header", style={'background-color': 'rgba(255, 255, 255, 0.4)','height': '288px','padding': '16px 0 0 0'}
       ),
        #html.Br(),
        # html.H1(children='Number of Citations about a Specific Keyword for a Faculty',style={"fontSize": "48px"},),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children='Keyword', className="menu-title", style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#41d7a7'}),# #079A82
                        dcc.Dropdown(
                            id='keyword1',
                            #style={'font-family': 'arial', 'text-align': 'center',"background-color":"white", "color": "blue"},
                            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'220px'},# DeepSkyBlue # #39cbfb
                            options=keywords_from_db,
                            value="data modeling",
                            clearable=False,
                            className="dropdown",
                        ),  dcc.Store(id='intermediate-value1')
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children='Faculty', className="menu-title", style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#41d7a7'}),
                        dcc.Dropdown(
                            id='faculty1',
                            #options=faculty_from_db,
                            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'220px'},
                            value="Teorey, Toby",
                            clearable=False,
                            className="dropdown",
                        ), dcc.Store(id='intermediate-value2'),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="From", className="menu-title" , style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#41d7a7'}
                    ),dcc.Dropdown(
                            id='date-range1',
                            #options=year_from_db,
                            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'100px'},
                            value=1989,
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="To", className="menu-title", style={ 'margin-bottom': '6px', 'font-weight': 'bold', 'color': '#41d7a7'}
                        ),
                        dcc.Dropdown(
                                id='date-range2',
                                #options=year_from_db,
                                style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'100px'},
                                value=2011,
                                clearable=False,
                                #searchable=False,
                                className="dropdown",
                            ),
                    ]
                ),
            ],
            className="menu", style={  'height': '112px','width': '912px','display': 'flex', 'justify-content': 'space-evenly', 'padding-top': '24px', 'margin': '-80px auto 0 auto','background-color': '#FFFFFF', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'}
        ),
        html.Div(
           children=[
               html.Div(
                   children=dcc.Graph(
                       id='citiations-chart',
                       config={"displayModeBar": False},
                   ),
                   className="card", style = {'margin-bottom': '24px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',},
                   )
           ],
           className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
       )
    ]
