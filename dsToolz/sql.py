# -*- coding: utf-8 -*-
import sys, logging
import pandas as pd
import pyodbc 

class ConnStrDB:
    def __init__(self, driver: str, server: str, database: str, uid: str, pwd: str):
        self.driver    =driver
        self.server    =server
        self.database  =database
        self.uid       =uid
        self.pwd       =pwd

        self.connStrAsDict = {
            'DRIVER'    : driver,
            'SERVER'    : server,
            'DATABASE'  : database,
            'UID'       : uid,
            'PWD'       : pwd,
        }

    def get(self):        
        return ";".join(f'{key}={val}' for key, val in self.connStrAsDict.items())


def readSqlQuery(sql_query: str, conn_string: ConnStrDB):
    try:
        
        conn = pyodbc.connect(conn_string.get())
        results = pd.read_sql_query(sql_query, conn)
        
        conn.close()        
    except Exception:
        logging.error(str(sys.exc_info()))
        sys.exit()
        
    return results