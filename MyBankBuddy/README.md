# MyBankBuddy

Bank Management System in Python with MySQL. This is a Python-based Bank Management System that allows users to create accounts, log in, and perform basic banking transactions such as checking balance, depositing money, and withdrawing money. The system uses MySQL to store customer and account data and bcrypt for password security.

### Features:  
1] Account Creation: Users can sign up with a username, password, and phone number. Account type selection (Savings/Current) is also available.  
2] Login System: Users log in using their phone number and password (passwords are hashed with bcrypt).

### Banking Operations:  
-> Check Balance: View current balance.  
-> Deposit Money: Deposit money into the account.  
-> Withdraw Money: Withdraw funds with sufficient balance checks.  
-> Transaction History: View all deposit and withdrawal transactions.  

MySQL Integration: The system uses MySQL to store customer data, account information, and transaction history.

### Requirements:  
Python 3.x  
MySQL database  
Required Python libraries: mysql-connector-python, bcrypt, termcolor, prettytable  

### How to Run:  
Step 1: Install the required libraries (for install Copy code: `pip install mysql-connector-python bcrypt termcolor prettytable`)  
Step 2: Set up a MySQL database and create necessary tables.  
Step 3: Run the script to start the system.
