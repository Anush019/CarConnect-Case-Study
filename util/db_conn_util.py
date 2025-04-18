import mysql.connector

class DBConnUtil:
    def __init__(self, host="localhost", user="root", password="root@123", database="CarConnect"):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values) if values else self.cursor.execute(query)
            self.conn.commit()
            print("DB Successful! !!")
            return self.cursor.rowcount
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")

    def fetch_query(self, query, values=None):
        try:
            self.cursor.execute(query, values) if values else self.cursor.execute(query)
            result = self.cursor.fetchall()
            if result:
                pass
            else:
                print("No records found.")
            return result
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            raise DatabaseConnectionException(f"Database fetch_one failed: {str(e)}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
