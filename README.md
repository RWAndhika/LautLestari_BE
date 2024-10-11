# FSSE-jan24_group-i_gfp_BE

This is a repository of the back-end for LautLestari, RevoU's Full-Stack Software Engineering (FSSE) Bootcamp group I final project.
*(Note: Due to the use of free services for the API, initial access may take a few moments.)*

For additional information and link of the Front-end:
[here](https://github.com/RWAndhika/LautLestari)

## API Documentation

[Postman API Documentation](https://documenter.getpostman.com/view/33841449/2sAXxS7Azj)

## Database Tables

```sql
CREATE DATABASE groupfinalproject;

USE groupfinalproject;

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
