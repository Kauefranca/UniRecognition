CREATE TABLE users (
    id INTEGER,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00,
    PRIMARY KEY(id)
);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE stocks (
    id INTEGER,
    owner_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC,
    total NUMERIC,
    buy_time DATETIME NOT NULL,
    sell_time DATETIME,
    PRIMARY KEY(id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE history (
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares TEXT NOT NULL,
    price numeric NOT NULL,
    transaction_time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- DELETE CHECK50 TESTS
DELETE FROM users WHERE id = 2;
DELETE FROM history WHERE user_id = 2;
DELETE FROM stocks WHERE owner_id = 2;