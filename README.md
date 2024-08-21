# FSSE-jan24_group-i_gfp_BE

## Database Table for now

```sql
DROP DATABASE groupfinalproject;

CREATE DATABASE groupfinalproject;

USE groupfinalproject;

DROP TABLE users;
DROP TABLE products;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    phonenumber VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE TABLE products(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    image VARCHAR(255),
    price INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    description VARCHAR(255),
    category VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    nationality VARCHAR(255) NOT NULL,
    referral_code VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE confirmations(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    buyer VARCHAR(255),
    product_id INTEGER,
    price INTEGER,
    qty INTEGER,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    is_confirm INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE subscribe(
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL
);
```
