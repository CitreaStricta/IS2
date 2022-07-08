from itsdangerous import NoneAlgorithm
import psycopg2

def get_db_connection():
    DBHOST="ec2-52-5-110-35.compute-1.amazonaws.com"
    DATABASE="d28t56b7dpk32k"
    DBUSER="zntctcuflomgsk"
    DBPASSWORD="43061258b91aaa3cf85b9c222443c57f889531d4478e8e0e69abcd715daf419c"
    DBPORT= "5432"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (DBHOST, DBPORT, DBUSER, DBPASSWORD, DATABASE)
    conn = psycopg2.connect(connstr)
    return conn

class Database:
    def __init__(self, db, user, password, port, host):
        self.db = db
        self.user = user
        self.password = password
        self.port = port 
        self.host = host

        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.password,
            port=self.port,
            host=self.host
        )
        self.cursor = self.connection.cursor()

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result
    
    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        self.connection.commit()
    
    def execute_returning(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        self.connection.commit()
        return result

    def close(self):
        self.cursor.close()
        self.connection.close()  