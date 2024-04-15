import psycopg2

# creating database named expenses

def create_database():

        conn = psycopg2.connect(dbname='postgres', password='120204', port=5432, user='postgres')
        conn.autocommit = True
        curr = conn.cursor()


        curr.execute("CREATE DATABASE expenses;")

        # conn.commit()
        conn.close()
        
        
        
def create_table():

        conn = psycopg2.connect(dbname='expenses', password='120204', port=5432, user='postgres')
        conn.autocommit = True
        curr = conn.cursor()

        query = '''CREATE TABLE expense_details (id serial PRIMARY KEY, date varchar(20), amount int, category varchar(20), description varchar(40));'''

        curr.execute(query)

        # conn.commit()
        conn.close()

create_database()
create_table()
