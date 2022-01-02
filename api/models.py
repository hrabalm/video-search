from db import conn, cursor

class Tables:
    @staticmethod
    def get_all():
        cursor.execute("SELECT * FROM pg_catalog.pg_tables")
        x = cursor.fetchall()
        return {"tables": x}

class Tags:
    @staticmethod
    def get_all():
        return {"tags": ["cat", "dog", "horse", "zebra"]}