# Project : Faculty Analytics

**Title: Name of your application.**

Faculty Analytics: Find the Faculty you want to connect!

**Purpose: What is the application scenario? Who are the target users? What are the objectives?**

The application scenarios involve users who are interested in connecting with a professor due to shared research interests, as well as professors who are seeking a university to join. 

The intended users of this application are professors who need research interest analytics for computer science faculty at universities in the United States. Moreover, professors who wish to add faculty to their university are also considered as target users.

The objectives of the application are to provide users with the ability to search for professors and access information about their research interests, publication history, and citation numbers. Additionally, users have the ability to add new professors to their university and remove professors who have left.

**Demo:**

https://mediaspace.illinois.edu/media/t/1_uhjjx6f1


**Installation: How to install the application?**

The application utilizes several modules such as dash, neo4j, pandas, sqlalchemy, pymongo, plotly, flask, pymysql, certifi, geopy, dash-bootstrap-components. Make sure to install all of them before running the application.

Follow the instructions provided in MP3 and MP4 to set up the three databases - mongodb, neo4j, and mysql. To access each database, change the default path of each DB and credentials in each utils file.

For installing the Neo4j APOC Library, click on the 'CS411 DBMS' database in Neo4j Desktop, go to plugins and install APOC. Then, click "..." -> Open Folder -> Configuration, create a new file in the config folder called 
**apoc.conf** and add the following 3 lines:
```
apoc.trigger.enabled = true
apoc.import.file.enabled = true 
apoc.export.file.enabled = true
```
Afterwards, restart the database. 

*NOTE:* It is important to keep the Neo4j database running in the background as most Neo4j features will not work otherwise.

To run the application, run **python app.py**, then open http://localhost:8050/ or equivalently: http://127.0.0.1:8050/

**Usage: How to use it?**

●	The "Citations number trend on a line chart" widget allows users to select a keyword, faculty name, and year range to visualize the citation number of publications related to the keyword from the professor. 

●	The "Find publication by keyword" widget prompts users to input a keyword for the search area. It returns a table containing publication information and a list of authors. 

●	The "Find publication by faculty name" widget prompts users to type a faculty member's name in the search area. It returns a table containing all their publications sorted by number of citations and year.

●	The "Compare Keywords interested in Different Institutes" widget displays a sunburn chart depicting the total number of faculty interested in specific keywords from the center, with faculty names on the outer rings. Users can modify the chart by adding or deleting keywords and institute names in the dropdowns. 

●	The "CS Faculty Count in US Map" widget displays universities with professors in the CS department classified into 0-50, 51-100, and so on. Users can view university names, CS faculty count, and geo location by hovering over the markers on the map. 

●	The "Find the Faculty Data" widget displays two cards: one is a datatable showing faculty contact information and their top five interest keywords, while the other displays the faculty's name, position, and photo. Users can search for different faculty by selecting institutes and faculty names in the dropdowns. 

●	In the "Modify Faculty" section, the "Add Faculty" widget allows users to input five basic properties for a faculty. If a new faculty information is added, a model will show the success information. 

●	The "Delete Faculty" widget allows users to delete a faculty from a university by entering their name and the university name. If a faculty information is deleted, a model will show the success information. 

●	Users can access raw college and faculty information at http://127.0.0.1:8050/college_and_faculty or view faculty and keyword data at http://127.0.0.1:8050/faculty_and_keyword.

**Design: What is the design of the application? Overall architecture and components.**

The application involves 8 independent widgets using the Dash. The widgets could divided into two categories: querying and updating backend databases. The querying widgets include show citation trends, sunburst chart, a college on US map, display faculty, search publication by keyword, and search publication by faculty. The updating widgets include add faculty and delete a faculty.

●	The line chart widget used neo4j and mysql The dropdown queries were performed in neo4j, and the line chart was created from the data query in mysql.

●	The Find the publication by keyword widget used mysql database to query publications based on keyword input. The query joined multiple tables, providing abundant information including all authors of the publication, processed based on the dataframe returned from mysql query.

●	The Find the publication by faculty widget used mysql database to query publications based on faculty input. A callback function was used to return the data.

●	The Sunburst Chart widget used Neo4j database, with functions written to retrieve all keywords and institutes. Callback functions were used to interactively generate the chart showing the percentage of faculties in certain keyword areas.

●	The college on map widget used MongoDB database, with external API calls used to generate geography data for each university. To speed up performance, cache was used to save all information in a CSV file.

●	The Display Faculty widget used Neo4j database to query data, with callback functions used to generate two cards showing the data.

●	The Add Faculty widget used Neo4j database to query and add new faculty node and university node, creating a relationship edge between these new nodes. A callback function was used to show success/fail query information in the model.

●	The Delete Faculty widget used Neo4j database to query and delete the relationship edge between faculty node and university node, then delete the faculty node. A callback function was used to show success/fail query information in the model.

**Implementation: How did you implement it? What frameworks and libraries or any tools have you used to realize the dashboard and functionalities?**

The application has integrated Dash and dash-bootstrap-components for the frontend, which includes features such as maps, line graphs, dropdowns, sunburst charts and data tables. 

On the backend, the Dash app serves as the main application server based on Flask app. The "dbs" module contains all Python files related to database utilities, while "widgets" contains all Python files related to 8 widgets. 

Regarding the database, "neo4j_util.py" is used to connect to Neo4j database, "mongodb_util.py" to connect to MongoDB database, and "MySQL_util.py" to connect to MySQL database. 

The application utilizes several libraries including dash, neo4j, pandas, sqlalchemy, pymongo, plotly, flask, pymysql, certifi, geopy, and dash-bootstrap-components to achieve its functionality. RESTful API based on Flask app was used to wrap around Dash, with several routes registered to support restful API calls. 

**Database Techniques: What database techniques have you implemented?**

●	Indexing

●	View

●	Constraint

●	Trigger

●	REST API for accessing databases


**Database Techniques: How?**

●	Indexing: created an index on the keyword name / institute name in order to enhance query performance in Neo4j.

```
"CREATE INDEX node_range_keyword_name IF NOT EXISTS FOR (n:KEYWORD) ON (n.name)"
```

```
"CREATE INDEX node_range_keyword_name IF NOT EXISTS FOR (n:INSTITUTE) ON (n.name)"
```

●	View: created a view for multiple table joins to expedite query processing time in MySQL.
  
```
"CREATE OR REPLACE VIEW TempView AS SELECT pub.num_citations, pub.year, f.name as professor_name, k.name as keyword_name FROM keyword k inner join publication_keyword pub_k on k.id = pub_k.keyword_id inner join publication pub on pub_k.publication_id = pub.id inner join faculty_publication fp on pub.id = fp.publication_id inner join faculty f on fp.faculty_id = f.id WHERE pub.id > 0;"

```

●	Constraint: implemented a constraint before adding new nodes to maintain data integrity in Neo4j.

```
"CREATE CONSTRAINT faculty_name1 IF NOT EXISTS FOR (f:FACULTY) REQUIRE f.name IS NOT NULL"
 ```

```
"CREATE CONSTRAINT institute_name IF NOT EXISTS FOR (i:INSTITUTE) REQUIRE i.name IS NOT NULL"
 ```

●	Trigger: created a trigger before adding a node to perform a check on the faculty ID increment, and created a trigger to count number of deletion to maintain data consistency in Neo4j. 

```
"CALL apoc.trigger.add('triggeredID', 'UNWIND $createdNodes AS e MATCH(f:FACULTY) with e, MAX(f.ID) as maxId Set e.ID = maxId + 1', {phase:'before'});"
```
```
"CALL apoc.trigger.add('count-removals','MATCH (c:Counter) SET c.count = c.count + size([f IN $deletedNodes WHERE id(f) > 0])',{});"
```           

●	REST API for accessing databases: developed Flask API endpoints with the server object and registered several routes to support RESTful API calls. 


**Extra-Credit Capabilities: What extra-credit capabilities have you developed, if any?**

●	Multi-database querying: The "Citations number trend on a line chart" function involves querying two databases. It involves filling in four dropdowns using Neo4j and then querying MySQL to obtain the line chart.

●	External data sourcing: the "CS Faculty Count in US Map" widget requires external data sourcing by querying the Google geopy library to bring in geographic data to support the widget. 


**Contributions: How each member has contributed, in terms of 1. tasks done and 2. time spent?**

Implemented 8 widgets (including Frontend, Backend and Databases) ~ Each widget tooks about 8 hours average

Recorded, edited Video and write README report - tooks 8 hours
