import sqlite3
from sqlite3 import Error 
import config 

def sql_connection():
    try:
      con = sqlite3.connect(config.db, check_same_thread=False)
      return con
    except Error:
      print(Error)

def initial_table_creation(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS filters(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, value TEXT)")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS videos(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, value TEXT)")
    con.commit()
    con.commit()

# filters
def insert_filter(con, filter_name, filter_type, filter_value):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO filters(name,type,value)VALUES(?, ?, ?)", (filter_name, filter_type, filter_value))
    con.commit()

def get_filters(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM filters")
    rows = cursorObj.fetchall()
    return rows

def delete_filter(con, filter_id):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM filters WHERE id = ?",(filter_id))
    con.commit()

def edit_filter(con, filter_id, filter_name, filter_type, filter_value):
    cursorObj = con.cursor()
    cursorObj.execute("UPDATE filters SET name = ?, type = ?, value = ? WHERE id = ?",(filter_name, filter_type, filter_value, filter_id))
    con.commit()