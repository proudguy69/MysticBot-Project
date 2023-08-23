# this will contain class and methods to set up and alter the postgres database
import asyncpg

class Database():
    
    def createDatabase():
        asyncpg.connect()