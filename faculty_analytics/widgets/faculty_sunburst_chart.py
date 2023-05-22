from dash import dcc, html, Dash, Input, Output
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
from academic_world_project.dbs.neo4j_utils import get_institutes, get_keywords, get_selection_items1

# from uiuc_411_project.db.mysql import MYSQL

def generate_faculty_pie_chart(app: Dash) -> list:
    @app.callback(
        Output("keywords_institute_pie", "figure"),
        Input("keywords", "value"),
        Input("institutes", "value")
    )
    def generate_keywords_selection_pie(keywords_input, institutes_input):
        result = get_selection_items1(keywords_input, institutes_input)
        df = pd.DataFrame(result, columns=['keywords', 'institutes','faculty_name', 'faculty_count'], dtype=str)
        #fig = px.pie(df, values="faculty_count", names="institutes", hole=.3)
        fig = px.sunburst(df, path=['institutes','keywords','faculty_name'], values='faculty_count')
        

        return fig
    '''
    def generate_keywords_selection_pie_map(keywords_input, institutes_input):
        result1 = get_selection_items1(keywords_input, institutes_input)
        mysql = MYSQL()
        placeholder1= ', '.join(str(unused) for unused in keywords_input)
        placeholder2= ', '.join(str(x[2]) for x in result1)
        result2 = mysql.get_publication_by_faculty_keyword(placeholder2,placeholder1, 0)
        df1 = pd.DataFrame(result1, columns=['keywords', 'institutes','faculty_name', 'faculty_count'], dtype=str)
        df2 = pd.DataFrame(result2, columns=['publication_name','professor_id','professor_name','keyword_name'], dtype=str)
        results = pd.merge(df1, df2, how='left', left_on=['keywords','faculty_name'], right_on =['keyword_name', 'professor_name'])
        #df = pd.DataFrame(results, columns=['keywords', 'institutes','faculty_name', 'faculty_count'], dtype=str)
        #fig = px.pie(df, values="faculty_count", names="institutes", hole=.3)
        fig = px.sunburst(results, path=['institutes','keywords','faculty_name','publication_name'], values='faculty_count')
        fig = go.Figure()

        fig.add_trace(go.Sunburst(
            ids=results.institutes,
            labels=results.keywords,
            parents=results.faculty_name,
            domain=dict(column=4)
        ))

        return fig
    '''

    keywords_from_db = get_keywords()
    institutes_from_db = get_institutes()
    return [
        html.H1('Compare Keywords interested in Different Institutes',style={'textAlign': 'center'}),
        #html.Br(),
        
        html.H2(children='Select your Keywords',style={'textAlign': 'center'}),
        
        html.Div(
            children=dcc.Dropdown(
            id='keywords',
            options=keywords_from_db,
            value=['internet', 'computer science'],
            multi=True,
            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'880px'},
            
        ),
        style=dict(display='flex', justifyContent='center')
        ),
        #html.Br(),
        html.H2(children='Select your Institutes' ,style={'textAlign': 'center'}),
     
        html.Div(
            children=dcc.Dropdown(
            id='institutes',
            options=institutes_from_db,
            value=['Purdue University--West Lafayette', 'University of Rochester', 'University of California--Berkeley','Johns Hopkins University'],
            multi=True, 
            style={'font-family': 'arial', "background-color":"white", "color": "DeepSkyBlue",'width':'880px'},
            
            ),
        style=dict(display='flex', justifyContent='center')
        ),
        # html.H3(children='Result'),
       # dcc.Graph(id='keywords_institute_pie')
        html.Div(
           children=[
               html.Div(
                   children=dcc.Graph(id='keywords_institute_pie',
                       config={"displayModeBar": False},
                   ),
                   className="card", style = {'margin-bottom': '24px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',},
                   )
           ],
           className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
       )
    ]
