CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL
);

INSERT INTO accounts (user_id, username, password, email)
VALUES (1, 'Tom B. Erichsen', 'Skagen 21', 'Stavanger@gmail.com');

INSERT INTO accounts (user_id, username, password, email)
VALUES (2, 'test B. Erichsen', 'test 21', 'test@gmail.com');

INSERT INTO accounts (user_id, username, password, email)
VALUES (3, 'test1 B. Erichsen', 'test 21', 'test1@gmail.com');

INSERT INTO accounts (user_id, username, password, email)
VALUES (4, 'test2 B. Erichsen', 'test 2', 'test2@gmail.com');