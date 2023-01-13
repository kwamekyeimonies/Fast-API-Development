import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv() 


def connect_to_database():
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    cursor_factory=RealDictCursor
    
    database_connection= psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port,
        cursor_factory=cursor_factory
    )
    
    return database_connection

def create_table(db_conn):
    cursor = db_conn.cursor()    
    cursor.execute(
    """ 
    CREATE TABLE IF NOT EXISTS products(
        name VARCHAR(255),
        price INTEGER,
        id serial PRIMARY KEY,
        is_sale BOOLEAN,
        inventory INTEGER,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()        
    );
    """
    )
    
    cursor.commit()
    db_conn.commit()
    cursor.close()