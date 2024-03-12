import pymysql

def get_connection_sql():
    return pymysql.connect(host="localhost", port=3306, user="test_user", password="123456", database="test_data", charset="utf8")