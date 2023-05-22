from dash import dcc, html, Dash, Input, Output, State
from dash.exceptions import PreventUpdate
from academic_world_project.dbs.neo4j_utils import delete_a_faculty_member
import dash_bootstrap_components as dbc


def generate_delete_faculty(app: Dash) -> list:
    @app.callback(
        Output('delete_faculty_result1', 'children'),
        Output('delete_faculty_result2', 'children'),
        Output('input_name2', 'value'),
        Output('input_institute_name2', 'value'),
        Output("modal-lg2", "is_open"),
        Input('submit-val2', 'n_clicks'),
        State('input_name2', 'value'),
        State('input_institute_name2', 'value'),
        State("modal-lg2", "is_open"),
    )
    def delete_a_new_faculty(n_clicks, name2, institute_name2, is_open):
        try:
            if n_clicks > 0: # name is not None and institute_name is not None:
                delete_a_faculty_member(name2, institute_name2)
                return " ✅ Successfully deleted a new faculty member!",f"Well done! You successfully deleted {name2} from {institute_name2}.", '', '', not is_open
        except Exception as e:
            print(f"Error occurred due to: {e}")
            return " ❌ Failed to delete a new faculty member.", "Oh snap! Change a few things up and try submitting again.",name2, institute_name2, not is_open
        raise PreventUpdate

    return [
        html.Br(),
        html.H2('Delete a Faculty Member',style={'textAlign': 'center'}),
        html.Div(children=[
           html.Div(children=dbc.Table([
            html.Thead(html.Tr([
                html.Th('Faculty Fields',style={'textAlign': 'center'}),
                html.Th('Faculty Values',style={'textAlign': 'center'})
            ])),
            html.Tbody([html.Tr([
                html.Td('Name',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_name2',
                    type='text',
                    placeholder='Enter a faculty name here'
                ))
            ]),
            html.Tr([
                html.Td('Institute Name',style={'textAlign': 'center'}),
                html.Td(dbc.Input(
                    id='input_institute_name2',
                    type='text',
                    placeholder='Enter an institute name here'
                 ))
             ])
             ])
         ],color="active",bordered=True,hover=True,responsive=True, size='lg' 
         ),
        ),
         html.Div([
         dbc.Button('Submit', id='submit-val2', n_clicks=0, color="secondary",size="lg", className="me-1"),
    ],
     className="d-grid gap-2", #"d-grid gap-2 col-6 mx-auto",
 ),
     ],
     className="wrapper", style = {'margin-right': 'auto','margin-left': 'auto','max-width': '1024px', 'padding-right': '10px', 'padding-left': '10px', 'margin-top': '32px',}
 ),
         dbc.Modal(
             [
                 dbc.ModalHeader(dbc.ModalTitle(id="delete_faculty_result1", children='')),
                 dbc.ModalBody( id="delete_faculty_result2", children=''),
             ],
             id="modal-lg2",
             size="lg",
             is_open=False,
         ),
     ]
    
