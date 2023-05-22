import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text

from academic_world_project.dbs.load_db import dbloader


class MYSQL:
    def __init__(self):
        secret = dbloader('mysql')
        host = secret.host
        user = secret.user
        password = secret.password
        database = secret.db
        port = secret.port
        charset = secret.charset
        self.connection = sa.create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}")

    def get_publication_by_keyword(self, keyword, last_id) -> pd.DataFrame:
        query = f"select distinct pub.id as publication_id, pub.title as publication_name, pub.year as year, faculty.name as professor from keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty on fp.faculty_id = faculty.id WHERE k.name = '{keyword}' AND pub.id > {last_id} ORDER BY pub.id LIMIT 50"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['publication_id', 'publication_name', 'year', 'professor'])

        unique_paper_ids = dict()
        duplicate_index_ids = list()
        index = 0
        while index < len(df):
            paper_id = df['publication_id'].values[index]
            if paper_id not in unique_paper_ids:
                unique_paper_ids[paper_id] = index
            else:
                duplicate_index_ids.append(index)
                df.at[unique_paper_ids[paper_id], 'professor'] += " | " + df['professor'].values[index]
            index += 1
        df = df.drop(labels=duplicate_index_ids)
        return df
    
    def get_year_by_faculty(self, keyword, faculty) -> pd.DataFrame:
        connection = self.connection.connect()
        sql = "CREATE OR REPLACE VIEW TempView AS SELECT pub.num_citations, pub.year, f.name as professor_name, k.name as keyword_name FROM keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE pub.id > 0;"
        connection.execute(text(sql))
        query = f"select distinct year as year from TempView WHERE keyword_name = '{keyword}' AND professor_name = '{faculty}' ORDER BY year "
        # query = f"select sum(pub.num_citations) as num_of_citiations, pub.year as year, f.name as professor_name, k.name as keyword_name from keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE k.name = '{keyword}' AND f.name = '{faculty}' AND pub.id > {last_id} AND pub.year >= {start_date} and pub.year <= {end_date} GROUP BY f.name, k.name, pub.year ORDER BY pub.year "
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['year'])
        df1 = df
        sql2 = "DROP VIEW IF EXISTS TempView"
        connection.execute(text(sql2))

        return df,df1
    
    def get_publication_by_faculty_keyword1(self, faculty, keyword, last_id, start_date, end_date) -> pd.DataFrame:
        connection = self.connection.connect()
        sql = f"CREATE OR REPLACE VIEW TempView AS SELECT pub.num_citations, pub.year, f.name as professor_name, k.name as keyword_name FROM keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE pub.id > {last_id};"
        connection.execute(text(sql))
        query = f"select sum(num_citations) as num_of_citiations, year as year, professor_name, keyword_name from TempView WHERE keyword_name = '{keyword}' AND professor_name = '{faculty}' AND year >= {start_date} and year <= {end_date} GROUP BY professor_name, keyword_name, year ORDER BY year "
        # query = f"select sum(pub.num_citations) as num_of_citiations, pub.year as year, f.name as professor_name, k.name as keyword_name from keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE k.name = '{keyword}' AND f.name = '{faculty}' AND pub.id > {last_id} AND pub.year >= {start_date} and pub.year <= {end_date} GROUP BY f.name, k.name, pub.year ORDER BY pub.year "
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['num_of_citiations','year','professor_name','keyword_name'])
        sql2 = "DROP VIEW IF EXISTS TempView"
        connection.execute(text(sql2))

        return df
    
    def get_publication_by_faculty_keyword(self, faculty_list, keyword_list, last_id) -> pd.DataFrame:
        query = f"select pub.title as publication_name, f.name as professor_name, f.id as professor_id, k.name as keyword_name from keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE k.name IN ('{keyword_list}') AND f.name IN ('{faculty_list}') AND pub.id > {last_id} ORDER BY professor_id, keyword_name, pub.year DESC LIMIT 3"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['publication_name','professor_id','professor_name','keyword_name'])

        unique_paper_ids = dict()
        duplicate_index_ids = list()
        index = 0
        while index < len(df):
            paper_id = df['publication_id'].values[index]
            if paper_id not in unique_paper_ids:
                unique_paper_ids[paper_id] = index
            else:
                duplicate_index_ids.append(index)
                df.at[unique_paper_ids[paper_id], 'professor'] += " | " + df['professor'].values[index]
            index += 1
        df = df.drop(labels=duplicate_index_ids)
        return df
    
    
    def get_publication_by_faculty(self, faculty, last_id) -> pd.DataFrame:
        query = f"select distinct pub.id as publication_id, pub.title as publication_name, pub.year as year, pub.num_citations as num_of_citations, f.name as professor from publication pub inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE f.name = '{faculty}' AND pub.id > {last_id} ORDER BY num_of_citations DESC, year DESC LIMIT 50"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['publication_id', 'publication_name', 'year', 'num_of_citations','professor'])

        unique_paper_ids = dict()
        duplicate_index_ids = list()
        index = 0
        while index < len(df):
            paper_id = df['publication_id'].values[index]
            if paper_id not in unique_paper_ids:
                unique_paper_ids[paper_id] = index
            else:
                duplicate_index_ids.append(index)
                df.at[unique_paper_ids[paper_id], 'professor'] += " | " + df['professor'].values[index]
            index += 1
        df = df.drop(labels=duplicate_index_ids)
        return df

    def set_publication_review(self, paper_id, reviewer_id, score):
        params = [paper_id, score, reviewer_id]
        cursor = self.connection.raw_connection().cursor()
        cursor.callproc('UpsertPublicationReview', params)

    def get_publication_reviews(self, paper_id):
        query = f"select pub.id as publication_id, pub.title as publication_name, pr.score as review_score, pr.reviewer_id as reviewer from publication pub inner join publication_review pr on pub.id = pr.publication_id where pub.id = {paper_id} order by pr.score_id desc"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['publication_id', 'publication_name', 'review_score', 'reviewer'])
        return df

    def get_professor_ratings(self):
        query = "with faculty_ratings as ( " \
                "select distinct fp.faculty_id as fID,sum(pr.score) / count(*) as ratings " \
                "from publication pub inner join publication_review pr on pub.id = pr.publication_id inner join faculty_publication fp on pub.id = fp.publication_id " \
                "group by fp.faculty_id), " \
                "faculty_papers as ( " \
                "select fp.faculty_id as fID, count(*) as papers " \
                "from faculty_publication fp  " \
                "group by fp.faculty_id) " \
                "select distinct f.name as professor, uni.name as school, fr.ratings as ratings, fp.papers as papers " \
                "from faculty f inner join university uni on f.university_id = uni.id inner join faculty_ratings fr on f.id = fr.fID inner join faculty_papers fp on f.id = fp.fID"
        pandaQuery = pd.read_sql_query(query, self.connection)
        df = pd.DataFrame(pandaQuery, columns=['professor', 'school', 'ratings', 'papers'])
        return df





