import os
import sqlalchemy
from flask import Flask

app = Flask(__name__)

def init_unix_connection_engine(**db_config):
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    
    
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
    
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user, 
            password=db_pass, 
            database=db_name,
            query={"unix_sock": "{}/{}/.s.PGSQL.5432".format(
                db_socket_dir,
                cloud_sql_connection_name)
            }
        ),
        **db_config
    )
    
    pool.dialect.description_encoding = None
    return pool

@app.route('/')
def main():

    db = init_unix_connection_engine(pool_size=5, max_overflow=2, pool_timeout=30, pool_recycle=1800)

    with db.connect() as conn:
        result = conn.execute().fetchall()

    return str(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)