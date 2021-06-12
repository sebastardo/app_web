import sqlite3

def create_db():
    cursor = None
    try:
        connection = sqlite3.connect("sqlite3.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE users(
                user_id integer NOT NULL,
                username character varying(50),
                password character varying(255),
                CONSTRAINT users_pkey PRIMARY KEY (user_id)
            )
            """)
    except Exception as error:
        print("Database:", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def select_query(query):
    cursor = None
    try:
        connection = sqlite3.connect("sqlite3.db")
        print("Connection successful")
        cursor = connection.cursor()
        cursor.execute(query)
        print("Query executed")
        result = cursor.fetchall()
        return result
    except Exception as error:
        print("Error connecting to data base.", error)
    finally:
        if cursor:
            cursor.close()
            print("Cursor closed")
        if connection:
            connection.close()
            print("Connection terminated")
    

def modify_query(query):
    cursor = None
    try:
        connection = sqlite3.connect("sqlite3.db")
        print("Connection successful")
        cursor = connection.cursor()
        cursor.execute(query)
        print("Query executed")
        connection.commit()
    except Exception as error:
        print("Error connecting to data base.", error)
    finally:
        if cursor:
            cursor.close()
            print("Cursor closed")
        if connection:
            connection.close()
            print("Connection terminated")

