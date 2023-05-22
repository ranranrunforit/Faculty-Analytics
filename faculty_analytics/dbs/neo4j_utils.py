from neo4j import GraphDatabase

DB_ADDRESS = "bolt://localhost:7687"
DB_AUTH = ("neo4j", "Zcr0906@") # password


def get_keywords() -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            keywords = []
            result = session.run('MATCH (keyword:KEYWORD) RETURN distinct keyword.name')
            for data in result.data():
                keywords.append(data['keyword.name'])
        driver.close()

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return keywords

def get_faculty(keyword: str) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculties = []
            result = session.run("MATCH (f:FACULTY)-[rp:PUBLISH]->(p:PUBLICATION)-[rl:LABEL_BY]->(k:KEYWORD)"
                                 f"where k.name = '{keyword}' AND p.year <> 0 "
                                 "RETURN distinct f.name")
            for data in result.data():
                faculties.append(data['f.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculties

def get_year(keyword: str, faculty: str) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            session.run("CREATE INDEX node_range_keyword_name IF NOT EXISTS FOR (n:KEYWORD) ON (n.name)")
            years1, years2 = [], []
            result = session.run("MATCH (f:FACULTY)-[rp:PUBLISH]->(p:PUBLICATION)-[rl:LABEL_BY]->(k:KEYWORD) "
                                 f"WHERE f.name = '{faculty}' AND k.name = '{keyword}' AND p.year <> 0 "
                                 "RETURN distinct p.year ORDER BY p.year")
            for data in result.data():
                years1.append(data['p.year'])
        years2 = years1
        driver.close()

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    
    return years1,years2

def get_institutes() -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            session.run("CREATE INDEX node_range_keyword_name IF NOT EXISTS FOR (n:INSTITUTE) ON (n.name)")
            institutes = []
            result = session.run('MATCH (i:INSTITUTE) RETURN i.name')
            for data in result.data():
                institutes.append(data['i.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return institutes

'''
def get_selection_items(keywords: list, institutes: list) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            results = []
            keywords_str = "','".join(keywords)
            institutes_str = "','".join(institutes)
            result_2 = session.run("match (faculty:FACULTY)-[r:INTERESTED_IN]->(keyword:KEYWORD), "
                                   "(faculty:FACULTY)-[af:AFFILIATION_WITH]->(i:INSTITUTE) "
                                   "with keyword as keyword,count(faculty.name) as faculty_count, i.name as institute "
                                   f"where institute in ['{institutes_str}'] and keyword.name in ['{keywords_str}']  "
                                   "return keyword, institute, faculty_count order by faculty_count desc")
            for data in result_2.data():
                results.append([data["keyword"]["name"], data["institute"], data["faculty_count"]])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return results
'''
def get_selection_items1(keywords: list, institutes: list) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            results = []
            keywords_str = "','".join(keywords)
            institutes_str = "','".join(institutes)
            result_2 = session.run("match (faculty:FACULTY)-[r:INTERESTED_IN]->(keyword:KEYWORD), "
                                   "(faculty:FACULTY)-[af:AFFILIATION_WITH]->(i:INSTITUTE) "
                                   "with keyword as keyword, faculty.name as faculty_name, count(DISTINCT faculty.name) as faculty_count, i.name as institute "
                                   f"where institute in ['{institutes_str}'] and keyword.name in ['{keywords_str}']  "
                                   "return keyword, institute, faculty_name, faculty_count order by faculty_count desc")
            for data in result_2.data():
                results.append([data["keyword"]["name"], data["institute"],data["faculty_name"], data["faculty_count"]])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return results

def get_faculties(institute: str) -> list:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculties = []
            result = session.run("MATCH (f:FACULTY)-[r:AFFILIATION_WITH]->(i:INSTITUTE) "
                                 f"where i.name = '{institute}' "
                                 "RETURN f.name")
            for data in result.data():
                faculties.append(data['f.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculties


def get_faculty_data(faculty_name: str) -> dict:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            faculty_all_info = {}
            result = session.run("match (f:FACULTY)-[af:AFFILIATION_WITH]->(i:INSTITUTE) "
                                 f"where f.name in ['{faculty_name}'] "
                                 "return f.photoUrl, f.phone, f.position, f.email, i.name")
            for data in result.data():
                faculty_all_info["photoUrl"] = data.get("f.photoUrl", "")
                if data.get("f.phone", "") is not None:
                    faculty_all_info["phone"] = data.get("f.phone", "").split(" ")[1]
                else:
                    faculty_all_info["phone"] = data.get("f.phone", "")
                faculty_all_info["position"] = data.get("f.position", "")
                faculty_all_info["email"] = data.get("f.email", "")
                faculty_all_info["institute_name"] = data.get("i.name", "")
            f_keys = []
            result2 = session.run("MATCH (f:FACULTY)-[r:INTERESTED_IN]->(k:KEYWORD) "
                                 f"WHERE f.name = '{faculty_name}' "
                                 "RETURN k.name ORDER BY r.score DESC LIMIT 5;")
            for data in result2.data():
                f_keys.append(data['k.name'])
        driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)
    return faculty_all_info, f_keys

def add_a_faculty_member(name, phone, position, email, institute_name) -> None:
    driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
    with driver.session(database='academicworld') as session:
        session.run(
        "CREATE CONSTRAINT faculty_name1 IF NOT EXISTS FOR (f:FACULTY) REQUIRE f.name IS NOT NULL"
        )
        session.run(
            "CALL apoc.trigger.add('triggeredID', 'UNWIND $createdNodes AS e MATCH(f:FACULTY) with e, MAX(f.ID) as maxId Set e.ID = maxId + 1', {phase:'before'});"
        )
        session.run(
            "CREATE CONSTRAINT institute_name IF NOT EXISTS FOR (i:INSTITUTE) REQUIRE i.name IS NOT NULL"
        )
        session.run(
            "MERGE (f:FACULTY {{name: '{name}', phone: '{phone}', position: '{position}', email: '{email}'}})"
            .format(name=name, phone=phone, position=position, email=email)
        )
        session.run(
            "MERGE (i:INSTITUTE {{name: '{institute_name}'}})".format(institute_name=institute_name)
        )
        
        session.run(
            "MATCH (f:FACULTY), (i:INSTITUTE) WHERE f.name = '{name}' AND i.name = '{institute_name}' "
            "MERGE (f)-[r:AFFILIATION_WITH]->(i)".format(name=name, institute_name=institute_name)
        )
        
        session.run(
            "CALL apoc.trigger.remove('triggeredID');"
        )
        
        session.run(
            "DROP CONSTRAINT faculty_name1 IF EXISTS;"
        )
        
        session.run(
            "DROP CONSTRAINT institute_name IF EXISTS;"
        )
        driver.close()


def delete_a_faculty_member(name, institute_name) -> None:
    try:
        driver = GraphDatabase.driver(DB_ADDRESS, auth=DB_AUTH)
        with driver.session(database='academicworld') as session:
            '''
            session.run(
                "CREATE (:Counter {count:0})"
            )
            session.run(
                "CALL apoc.trigger.add('count-removals','MATCH (c:Counter) SET c.count = c.count + size([f IN $deletedNodes WHERE id(f) > 0])',{});"
            )
            '''
            session.run(
                "MATCH (f:FACULTY)-[r:AFFILIATION_WITH]->(i:INSTITUTE) WHERE f.name = '{name}' AND i.name = '{institute_name}' DELETE r".format(name=name, institute_name=institute_name)
            )
            
            session.run(
                "MATCH (f:FACULTY) WHERE f.name = '{name}' DELETE f".format(name=name)
            )
            '''
            session.run(
                "MATCH (c:Counter) DELETE c;"
                )
            session.run(
                "CALL apoc.trigger.remove('count-removals');"
            )
            '''
            driver.close()
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(0)