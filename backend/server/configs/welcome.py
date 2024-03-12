from fastapi import APIRouter
from sql_config import get_connection_sql
welcome=APIRouter()


@welcome.get("/welcome",tags=["欢迎界面，default message"])
def get_homepage():
    return "default"

@welcome.get("/database",tags=["初始三个问题"])
def get_mysql():
    conn=get_connection_sql()
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT question ,number_of_question FROM test_question ORDER BY number_of_question DESC;")
        data=cursor.fetchmany(size=3)
    except Exception :
        print("error")
    finally:
        cursor.close()
    return [k for k in dict(data).keys()]