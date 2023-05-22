from collections import defaultdict
import csv
import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from academic_world_project.dbs.utils import get_college_geo_coordinates

DB_NAME = "academicworld"

fdir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH_COLLEGE= os.path.join(fdir,"college_faculty.csv")
FILE_PATH_FACULTY = os.path.join(fdir,"faculty_keywords.csv")
#FILE_PATH_COLLEGE= "/Users/chaor/Downloads/final project/mine/academic_world_Project-main/academic_world_project/dbs/college_faculty.csv"
#FILE_PATH_FACULTY = "/Users/chaor/Downloads/final project/mine/academic_world_Project-main/academic_world_project/dbs/faculty_keywords.csv"

def get_faculty_keyword(file_path: str = FILE_PATH_FACULTY) -> pd.DataFrame:

    if not os.path.exists(file_path):
        try:
            with open(file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["professors", "keywords"])
                client = MongoClient()
                collection = client[DB_NAME]["faculty"]
                names = collection.distinct("name")
                finfo = defaultdict(dict)
                for name in names:
                    try:
                        keywords = list(collection.find({"name": name}, { "_id": 0, "keywords.name": 1, "keywords.score" : 1}))
                        #keywords = list(collection.aggregate([{"$match": {"name": name}}, {"$unwind": '$keywords'}, { "$project":{ "_id": 0, "keywords.name": 1, "keywords.score" : 1}}]))
                        finfo[name]["keyword"] = keywords 
                        writer.writerow([name, keywords])
                    except Exception as e:
                        print(e)
        except ConnectionFailure as e:
            print(f"Failed to connect to mongodb due to: {e}")
            exit(0)
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            exit(0)
    return pd.read_csv(file_path)

def get_college_map(file_path: str = FILE_PATH_COLLEGE) -> pd.DataFrame:

    if not os.path.exists(file_path):
        query_mongodb_and_save_to_csv(file_path)
    return pd.read_csv(file_path)


def query_mongodb_and_save_to_csv(file_path: str = FILE_PATH_COLLEGE) -> None:

    try:
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["college", "professors", "lat", "lon"])

            # Connect to local mongo db
            client = MongoClient()
            collection = client[DB_NAME]["faculty"]
            names = collection.distinct("affiliation.name")
            us_map_info = defaultdict(dict)
            for name in names:
                try:
                    latitude, longitude = get_college_geo_coordinates(name)
                    professors = len(list(collection.find({"affiliation.name": name})))
                    us_map_info[name]["latitude"] = latitude
                    us_map_info[name]["longitude"] = longitude
                    us_map_info[name]["professors"] = professors
                    writer.writerow([name, professors, latitude, longitude])
                except Exception as e:
                    print(e)
    except ConnectionFailure as e:
        print(f"Failed to connect to mongodb due to: {e}")
        exit(0)
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        exit(0)
        


