import psycopg2 as db_connect
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def create_table():
    host_name = "localhost"
    db_user = "postgres"
    db_password = "Applekat166"
    db_name = "mh3y"
    connection = None
    try:
        connection = db_connect.connect(host=host_name, user=db_user, password=db_password, database=db_name)
        cursor = connection.cursor()

        query = "CREATE TABLE Persons (PersonID int PRIMARY KEY, LastName varchar(255), FirstName varchar(255), " \
                "Address varchar(255),City varchar(255));"

        cursor.execute(query)
        connection.commit()
        # results = cursor.fetchall()
        # print(results)

        connection.close()

    except db_connect.Error as err:
        print("Database Error", err)
    finally:
        if connection:
            connection.close()


def insert_persons(PersonID, LastName, FirstName, Address, City):
    query = "INSERT INTO Persons(PersonID,LastName, FirstName, Address, City) " \
            "VALUES(%s,%s,%s,%s,%s);"
    args = (PersonID, LastName, FirstName, Address, City)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def main():
    insert_persons('A Sudden Light', '9781439187036')
