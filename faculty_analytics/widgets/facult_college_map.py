from dash import html, dcc
import plotly.graph_objects as go

from academic_world_project.dbs.mongodb_utils import get_college_map


def _generate_us_college_map() -> go.Figure:
    df = get_college_map()
    df = df.sort_values(by=["professors"], ascending=False)
    df.head()

    df["text"] = "University: " + df['college'] + "<br>Number of professors: " + df['professors'].astype(str)
    #limits = [(0, 10),(11, 20), (21, 50), (51, 100), (101, 150), (151, 200),(200, 250),(251,300)]
    #colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
    #scale = 0.7
    
    
    fig = go.Figure(data=go.Scattergeo(
            locationmode = 'USA-states',
            lon=df["lon"],
            lat=df["lat"],
            text=df["text"],textposition="middle center",
            mode = 'markers',
            marker = dict(
                size = 8,#df["professors"]/6,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'Blues',
                cmin = 0,
                color = df['professors'],
                cmax = df['professors'].max(),
                colorbar_title="# of CS Faculty<br>"
            )))


    fig.update_layout(
            title = 'Computer Science Faculty Count in each University by State <br>(Hover for University name & Faculty Count)',
            geo = dict(
                scope='usa',
                projection_type='albers usa',
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
        
    
    '''
    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode="USA-states",
            lon=df_sub["lon"],
            lat=df_sub["lat"],
            text=df_sub["text"],
            marker=dict(
                size=df_sub["professors"]/scale,
                color=colors[i],
                line_color="rgb(40,40,40)",
                line_width=0.5,
                sizemode="area"
            ),
            name=f"{lim[0]} - {lim[1]}"
        ))
        
        fig.update_layout(
        title_text = 'Number of Computer Science professor in each University by State',
        showlegend=True,
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            landcolor="rgb(217, 217, 217)",
        )
    )
    '''
    
    return fig


def generate_college_map() -> list:
    return [
        html.H1(children='CS Faculty Count in US Map',style={'textAlign': 'center'}),
        #html.Br(),
        html.Div(children=[
               html.Div(
                   children=dcc.Graph(figure=_generate_us_college_map() ,config={"displayModeBar": False},),
                   className="card", style = {'margin-bottom': '24px', 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',},
                   )
               ],
                className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
            ),
    ]
