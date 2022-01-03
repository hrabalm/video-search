from db import conn, cursor, dict_cur
from pypika import Field, Query, Table, PostgreSQLQuery


class Tables:
    @staticmethod
    def get_all():
        q = """SELECT * FROM pg_catalog.pg_tables"""
        cursor.execute(q)
        x = cursor.fetchall()
        return {"tables": x}

class Tags:
    # @staticmethod
    # def get_all():
    #     return {"tags": ["cat", "dog", "horse", "zebra"]}

    @staticmethod
    def get_all():
        q = """SELECT id, tag, tag_type FROM tags"""
        dict_cur.execute(q)
        res = dict_cur.fetchall()
        res = [dict(x) for x in res]
        # return {"tags": ["cat", "dog", "horse", "zebra"], "raw": res}
        return {"tags": res}