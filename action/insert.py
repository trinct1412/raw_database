import os
from functools import reduce
from sqlalchemy import text
from ..base import BaseDatabase


class Insert(BaseDatabase):
    def __init__(self, connection, is_commit=True):
        self.connection = connection
        self.is_commit = is_commit
        self.__table = None
        self.__values = None
        self.__data = None
        self.__returning = None

    def __get_raw_sql(self):
        query = f"""
            INSERT INTO {self.__table}{self.__values}
        """
        query = query + f""" RETURNING {self.__returning} """ if self.__returning else query
        return text(query)

    def __set_values(self, values):
        key = reduce(lambda result, key_: result + f'{key_},', values, '')[:-1]
        value = reduce(lambda result, key_: result + f':{key_},', values, '')[:-1]
        self.__values = f"({key})VALUES({value})"

    def into(self, table, schema=None):
        self.__table = f"{schema}.{table}" if schema else table
        return self

    def values(self, **data):
        self.__set_values(data)
        self.__data = data
        return self

    def returning(self, key):
        self.__returning = key
        return self

    def execute(self):
        result = self.connection.execute(self.__get_raw_sql(), self.__data)
        if self.is_commit:
            self.connection.commit()
        return result

    def __getattr__(self, method_name):
        def execute():
            raw_sql = self.__get_raw_sql()
            result = self.execute()

            if method_name == 'execute':
                return result

            if os.getenv("IS_SHOW_SQL", False):
                self._show_query(raw_sql, self.__data)
            return getattr(result, method_name)()

        return execute
