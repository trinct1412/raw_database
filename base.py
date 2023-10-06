class BaseDatabase:
    def _get_query(self, raw_sql, parameters):
        try:
            self.__query = raw_sql.bindparams(**parameters).compile(compile_kwargs={"literal_binds": True})
            return self.__query
        except (Exception,) as _:
            self.__query = None

    def _show_query(self, raw_sql, parameters):
        print("----------------------------------------------------------")
        print(self._get_query(raw_sql, parameters))
        print("----------------------------------------------------------")

    @classmethod
    def equal(cls, value_condition, condition):
        if value_condition is None:
            return " IS "
        spliter = condition.split("__")
        if len(spliter) > 1:
            if spliter[1] == 'lte':
                return "<="
            if spliter[1] == 'gte':
                return ">="
            if spliter[1] == 'lt':
                return "<"
            if spliter[1] == "gt":
                return ">"
            return f" {' '.join(spliter[1:])} "
        return "="
