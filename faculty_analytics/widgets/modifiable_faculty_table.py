from dash import dcc, html, Dash, Input, Output, State
from dash.exceptions import PreventUpdate
from academic_world_project.dbs.neo4j_utils import add_a_faculty_member
import dash_bootstrap_components as dbc

def generate_modifiable_faculty(app: Dash) -> list:
    @app.callback(
        Output('add_faculty_result1', 'children'),
        Output('add_faculty_result2', 'children'),
        Output('input_name', 'value'),
        Output('input_phone', 'value'),
        Output('input_position', 'value'),
        Output('input_email', 'value'),
        Output('input_institute_name', 'value'),
        Output("modal-lg", "is_open"),
        Input('submit-val', 'n_clicks'),
        State('input_name', 'value'),
        State('input_phone', 'value'),
        State('input_position', 'value'),
        State('input_email', 'value'),
        State('input_institute_name', 'value'),
        State("modal-lg", "is_open"),
    )
    def add_a_new_faculty(n_clicks, name, phone, position, email, institute_name, is_open):
        try:
            if n_clicks > 0: # name is not None and institute_name is not None:
                add_a_faculty_member(name, phone, position, email, institute_name)
                return " ✅ Successfully added a new faculty member!",f"Well done! You successfully added {name} to {institute_name}.", '', '', '', '', '', not is_open
            #if name is None:
                #return "name could not be none"
            #elif institute_name is None:
                #return "institute name could not be none"
        except Exception as e:
            print(f"Error occurred due to: {e}")
            return " ❌ Failed to add a new faculty member.", "Oh snap! Change a few things up and try submitting again.",name, phone, position, email, institute_name, not is_open
        raise PreventUpdate
    
    

    return [
        html.H1('Modify Faculty',style={'textAlign': 'center'}),
        #html.Br(),
        html.H2('Add a New Faculty Member',style={'textAlign': 'center'}),
       
        html.Div(children=[
           html.Div(children=dbc.Table([
            html.Thead(html.Tr([
                html.Th('Faculty Fields',style={'textAlign': 'center'}),
                html.Th('Faculty Values',style={'textAlign': 'center'})
            ])),
            html.Tbody([html.Tr([
                html.Td('Name',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_name',
                    type='text',
                    placeholder='Enter a faculty name here'#, size='lg'
                ))
            ]),
            html.Tr([
                html.Td('Phone',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_phone',
                    type='text',
                    placeholder='Enter a phone number here'
                ))
            ]),
            html.Tr([
                html.Td('Position',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_position',
                    type='text',
                    placeholder='Enter a position here'
                ))
            ]),
            html.Tr([
                html.Td('Email',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_email',
                    type='text',
                    placeholder='Enter an email address here'
                ))
            ]),
            html.Tr([
                html.Td('Institute Name',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_institute_name',
                    type='text',
                    placeholder='Enter an institute name here'
                ))
            ])
            ])
        ],color="active",bordered=True,hover=True,responsive=True, size='lg' 
        ),
       ),
        html.Div([
        dbc.Button('Submit', id='submit-val', n_clicks=0, color="secondary",size="lg", className="me-1"),
   ],
    className="d-grid gap-2", #"d-grid gap-2 col-6 mx-auto",
),
    ],
    className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="add_faculty_result1", children='')),
                dbc.ModalBody( id="add_faculty_result2", children=''),
            ],
            id="modal-lg",
            size="lg",
            is_open=False,
        ),
    ]
