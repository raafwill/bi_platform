import psycopg2
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection(db_type, host, port, username, password, database):
    try:
        if db_type == 'postgres':
            conn_str = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == 'mysql':
            conn_str = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        else:
            return {'status': 'error', 'message': 'Unsupported database type'}

        engine = create_engine(conn_str)
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {'status': 'success', 'message': 'Connection successful'}
    except SQLAlchemyError as e:
        return {'status': 'error', 'message': str(e)}