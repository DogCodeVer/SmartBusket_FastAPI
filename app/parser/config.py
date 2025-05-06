import os

from dotenv import load_dotenv
from db.config import *

class Config:
    def __init__(self, dbconfig: DBConfig = DBConfig()) -> None:
        self.dbconfig = dbconfig

    def read_from_env(self):
        load_dotenv('.env')

        self.dbconfig = DBConfig(
            dbname=os.environ.get('SQL_DB', DEFAULT_DBNAME),
            user=os.environ.get("SQL_USER", DEFAULT_USER),
            pwd=os.environ.get("SQL_PWD", DEFAULT_PWD),
            host=os.environ.get("SQL_HOST", DEFAULT_HOST),
            port=os.environ.get("SQL_PORT", DEFAULT_PORT),

        )
