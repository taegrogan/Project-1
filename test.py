import pymysql
from creds import rds_host, db_user, db_password, db_name

try:
    conn = pymysql.connect(
        host=rds_host,
        user=db_user,
        password=db_password,
        db=db_name
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)