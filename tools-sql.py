import psycopg2 as db_connect

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
    # results = cursor.fetchall()
    # print(results)

    connection.close()

except db_connect.Error as err:
    print("Database Error", err)
finally:
    if connection:
        connection.close()
