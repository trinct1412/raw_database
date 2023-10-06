# Simple Module For Database

This is a simple Python module that provides functions to perform basic insert, update, and delete actions on a database.

## Installation

To use this module, you need to have Python installed on your system. You can install the module using pip:

```shell
pip install raw-database
```

## Usage
###### Import the module into your Python script:

    from raw_database import Insert, Update, QuerySet

## Insert Action
    
    Insert(connection, is_commit=False).into(table).values(**values).returning(return_key).fetchone()

* connection: Connection to database
* is_commit: Determine whether to commit this data
* table: The name of the table where the data will be inserted.
* values: A dictionary containing the data to be inserted, with column names as keys and corresponding values.
* return_key: A key will be return if insert is success

### Example usage:

    Insert(connection_, is_commit=False).into("accounts").values(user_id=6, username="Tom B", email="test email").returning("user_id").fetchone()

## Update Action

    Update(connection, is_commit=False)(table).set(**values).where(**conditions).returning(return_key).fetchone()

* connection: Connection to database
* is_commit: Determine whether to commit this data
* table: The name of the table where the data will be inserted.
* values: A dictionary containing the data to be inserted, with column names as keys and corresponding values.
* conditions: A dictionary containing conditions to update
* return_key: A key will be return if insert is success

### Example usage:

    Update(connection_, is_commit=False)(table="accounts").set(email="test email update", username="test username update").where(user_id=1).returning("user_id").fetchone()

## Get Action

    QuerySet(connection).select(*fields).from_(table).where(**condition).fetchone()

* connection: Connection to database
* fields: A list containing the selected from table
* table: The name of the table where the data will be inserted.
* conditions: A dictionary containing conditions to update

### Example usage:
    
    QuerySet(connection_).select("user_id", "username").from_("accounts").where(user_id=1).fetchone()
    QuerySet(connection_).select().from_("accounts").fetchall()
    QuerySet(connection_).select().from_("accounts").limit(2).fetchall()
    QuerySet(connection_).select().from_("accounts").order_by("user_id DESC").fetchall()
    QuerySet(connection_).select("user_id").from_("accounts").where(user_id__in=(1, 2, 3), username='Tom B. Erichsen').fetchall()
    QuerySet(connection_).select("user_id").from_("accounts").where(user_id__in=(1, 2, 3)).fetchall()
    QuerySet(connection_).select("password", "COUNT(*) AS same_password").from_("accounts").where(user_id__in=(1, 2, 3, 4)).group_by("password").fetchall()
    

# Contributing
###### Contributions are welcome! If you'd like to contribute to this module, please follow these steps:
* Fork the repository at [GitHub](https://github.com/trinct1412/raw_database).
* Create a new branch for your feature/bug fix.
* Make your changes and commit them.
* Push your changes to your fork.
* Submit a pull request.

