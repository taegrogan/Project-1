import pymysql
from creds import rds_host, db_user, db_password, db_name

def get_connection():
    return pymysql.connect(
        host=rds_host,
        user=db_user,
        passwd=db_password,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_movies_with_companies():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT movie.title, movie.release_date, production_company.name
                FROM movie
                JOIN movie_company ON movie.id = movie_company.movie_id
                JOIN production_company ON movie_company.company_id = production_company.id;
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        return {'error': str(e)}