from flask import Flask

from academic_world_project.dbs.mongodb_utils import get_college_map, get_faculty_keyword

flask_app = Flask(__name__)


def register_routes(app: Flask) -> None:
    @app.get("/faculty_and_keyword")
    def get_faculty_keyword_data():
        df = get_faculty_keyword()
        return df.to_dict(orient="split")

    @app.get("/college_and_faculty")
    def get_college_faculty_data():
        df = get_college_map()
        return df.to_dict(orient="split")


