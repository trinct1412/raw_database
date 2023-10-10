from raw_database import QuerySet, Insert, Update
from sqlalchemy import create_engine, URL

if __name__ == '__main__':
    url_connection = URL.create(
        "postgresql+psycopg2",
        username="root123",
        password="root123",
        host="localhost",
        database="test_db",
        port=5435,
    )

    connection_ = create_engine(url_connection).connect()
    a = QuerySet(connection_).select("user_id", "username").from_("accounts").where(user_id=1).fetchone()
    b = QuerySet(connection_).select().from_("accounts").fetchall()
    c = QuerySet(connection_).select().from_("accounts").limit(2).fetchall()
    d = QuerySet(connection_).select().from_("accounts").order_by("user_id DESC").fetchall()
    e = QuerySet(connection_).select("user_id").from_("accounts").where(user_id__in=(1, 2, 3),
                                                                        username='Tom B. Erichsen').fetchall()
    f = QuerySet(connection_).select("user_id").from_("accounts").where(user_id__in=(1, 2, 3)).fetchall()
    g = QuerySet(connection_).select("password", "COUNT(*) AS same_password").from_("accounts").where(
        user_id__in=(1, 2, 3, 4)).group_by("password").fetchall()

    # i = Insert(connection_, is_commit=False).into("accounts").values(user_id=8, username="Tomd B", password="test password",
    #                                                                 email="test email a").returning("user_id").fetchone()
    Insert(connection_, is_commit=True).into("accounts").values(user_id=8, username="Tomd B", password="test password").execute()
    # j = Update(connection_, is_commit=True)(table="accounts").set(email="test email update5", username="test u1sername updat1e").where(
    #     user_id=2).returning("user_id").fetchone()
    Update(connection_, is_commit=True)(table="accounts").set(email="test email update5", username="test u1sername updat1e").where(
        user_id=2).execute()