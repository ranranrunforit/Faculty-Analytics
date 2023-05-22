import json
import os

class dbloader:
    def __init__(self, databaseType):
        fdir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(fdir,"db.json")
        f = open(file_path)
        #secret_file_path = '/Users/chaor/Downloads/final project/mine/academic_world_Project-main/academic_world_project/dbs/db.json'
        #f = open(secret_file_path)
        self.secretData = json.load(f)
        self.loadSecretPerDBType(databaseType)

    def loadSecretPerDBType(self, databaseType):
        isDBTypeSupported = databaseType in self.secretData
        self.host = self.secretData[databaseType]['host'] if isDBTypeSupported else ''
        self.user = self.secretData[databaseType]['user'] if isDBTypeSupported else ''
        self.password = self.secretData[databaseType]['password'] if isDBTypeSupported else ''
        self.db = self.secretData[databaseType]['db'] if isDBTypeSupported else ''
        self.port = self.secretData[databaseType]['port'] if isDBTypeSupported else ''
        self.charset = self.secretData[databaseType]['charset'] if isDBTypeSupported else ''
