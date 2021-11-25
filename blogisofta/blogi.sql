/* blogitietokannan taulukon perustaminen */
CREATE TABLE posts (id SERIAL PRIMARY KEY, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, title TEXT NOT NULL, content TEXT NOT NULL);