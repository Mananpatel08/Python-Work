CREATE DATABASE BankManagment;
USE BankManagment;

CREATE TABLE Customers (
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) ,
    Password VARCHAR(255) ,
    phone_number VARCHAR(10) UNIQUE
);
CREATE TABLE Accounts (
	account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    phone_number VARCHAR(10) ,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (phone_number) REFERENCES Customers(phone_number),
    account_type VARCHAR(20) , 
    Balance DECIMAL(15,2) DEFAULT 0.00
);
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    amount DECIMAL(15, 2) ,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Type VARCHAR(20),
    BankBalance DECIMAL(15,2), 
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

SELECT * FROM Customers;
SELECT * FROM Accounts;
SELECT * FROM Transactions;

-- SET SQL_SAFE_UPDATES = 0;
