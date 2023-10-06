import os
from functools import reduce
from sqlalchemy import text
from ..base import BaseDatabase


class QuerySet(BaseDatabase):
    def __init__(self, connection):
        self.__fields = None
        self.__table = None
        self.__raw_conditions = None
        self.__conditions = None
        self.__query = None
        self.__limit = None
        self.__order_by = None
        self.__group_by = None
        self.__raw_having_conditions = None
        self.__having_conditions = None
        self.connection = connection

    def __get_raw_sql(self):
        query = f"""
            SELECT 
                    {self.__fields} 
            FROM 
                    {self.__table}
        """
        query = query + f""" WHERE {self.__raw_conditions} """ if self.__raw_conditions else query
        query = query + f""" GROUP BY {self.__group_by} """ if self.__group_by else query
        query = query + f""" HAVING {self.__raw_having_conditions} """ if self.__having_conditions else query
        query = query + f""" LIMIT {self.__limit}""" if self.__limit else query
        query = query + f""" ORDER BY {self.__order_by}""" if self.__order_by else query

        return text(query)

    def select(self, *fields):
        self.__fields = ",".join(fields) if fields else "*"
        return self

    def from_(self, table, schema=None):
        self.__table = f"{schema}.{table}" if schema else table
        return self

    def where(self, **conditions):
        self.__raw_conditions = reduce(
            lambda result,
                   condition: result + f"{condition.split('__')[0]} {self.equal(conditions[condition], condition)} :{condition} AND ",
            conditions, '')[:-len("AND ")]

        self.__conditions = conditions

        return self

    def limit(self, limit):
        self.__limit = limit
        return self

    def order_by(self, *orders):
        self.__order_by = ",".join(orders) if orders else None
        return self

    def group_by(self, *groups):
        self.__group_by = ",".join(groups) if groups else None
        return self

    def having(self, **conditions):
        self.__raw_having_conditions = reduce(
            lambda result,
                   condition: result + f"{condition.split('__')[0]} {self.equal(conditions[condition], condition)} :{condition} AND ",
            conditions, '')[:-len("AND ")]

        self.__having_conditions = conditions
        return self

    def __getattr__(self, method_name):
        def execute():
            raw_sql = self.__get_raw_sql()
            where_conditions = self.__conditions if self.__conditions else {}
            having_conditions = self.__having_conditions if self.__having_conditions else {}
            parameters = {**where_conditions, **having_conditions}
            args = (raw_sql, parameters) if parameters else (raw_sql,)
            if os.getenv("IS_SHOW_SQL", False):
                self._show_query(raw_sql, parameters)
            return getattr(self.connection.execute(*args), method_name)()

        return execute
