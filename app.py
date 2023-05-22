# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html
import dash_bootstrap_components as dbc

from academic_world_project.app_registrations import flask_app, register_routes
from academic_world_project.widgets.facult_college_map import generate_college_map
from academic_world_project.widgets.faculty_sunburst_chart import generate_faculty_pie_chart
from academic_world_project.widgets.view_faculty_table import generate_view_faculty
from academic_world_project.widgets.modifiable_faculty_table import generate_modifiable_faculty
from academic_world_project.widgets.faculty_publication_citiations_figure import publication_citiation
from academic_world_project.widgets.keyword_publication_list import get_publications_by_keyword
from academic_world_project.widgets.faculty_publication_list import get_publications_by_faculty
from academic_world_project.widgets.modifiable_faculty_table_delete import generate_delete_faculty 


register_routes(flask_app)
flask_app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app = Dash(__name__, server=flask_app,
                 external_stylesheets=[dbc.themes.QUARTZ,
                                 dbc.icons.BOOTSTRAP]
               )

app.title = "Faculty Analytics: Find the Faculty you want to connect!"

content = []

content.extend(publication_citiation(app))

content.extend(get_publications_by_keyword(app))

content.extend(get_publications_by_faculty(app))

content.extend(generate_view_faculty(app))

content.extend(generate_faculty_pie_chart(app))

content.extend(generate_college_map())

content.extend(generate_modifiable_faculty(app))

content.extend(generate_delete_faculty(app))


app.layout = html.Div(children=content)


if __name__ == '__main__':
    app.run_server(debug=True)
