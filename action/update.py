import os
from functools import reduce
from sqlalchemy import text
from ..base import BaseDatabase


class Update(BaseDatabase):
    def __init__(self, connection, is_commit=True):
        self.connection = connection
        self.is_commit = is_commit
        self.__modifies = None
        self.__conditions = None
        self.__raw_conditions = None
        self.__raw_modifies = None
        self.__table = None
        self.__returning = None

    def __call__(self, table, schema=None):
        self.__table = f"{schema}.{table}" if schema else table
        return self

    def __get_raw_sql(self):
        query = f"""
           UPDATE
               {self.__table}
           SET
               {self.__raw_modifies}
        """
        query = query + f""" WHERE {self.__raw_conditions} """ if self.__raw_conditions else query
        query = query + f""" RETURNING {self.__returning} """ if self.__returning else query
        return text(query)

    def set(self, **modifies):
        self.__raw_modifies = reduce(lambda result, key: result + f'{key}=:{key},', modifies, '')[:-1]
        self.__modifies = modifies
        return self

    def where(self, **conditions):
        self.__raw_conditions = reduce(
            lambda result,
                   condition: result + f"{condition.split('__')[0]} {self.equal(conditions[condition], condition)} :{condition} AND ",
            conditions, '')[:-len("AND ")]

        self.__conditions = conditions
        return self

    def returning(self, key):
        self.__returning = key
        return self

    def execute(self):
        parameters = {**self.__modifies, **self.__conditions}
        raw_sql = self.__get_raw_sql()
        result = self.connection.execute(raw_sql, parameters)
        if self.is_commit:
            self.connection.commit()
        return result

    def __getattr__(self, method_name):
        def execute():
            raw_sql = self.__get_raw_sql()
            parameters = {**self.__modifies, **self.__conditions}
            result = self.execute()
            if os.getenv("IS_SHOW_SQL", False):
                self._show_query(raw_sql, parameters)
            return getattr(result, method_name)()

        return execute
