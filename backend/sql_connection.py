import datetime
import mysql.connector

def get_sql_connection():
    """Return a new MySQL connection."""
    print("Opening mysql connection")
    return mysql.connector.connect(user='Geetha', password='Geetha@123', database='grocery_store')

