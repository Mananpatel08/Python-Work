import bcrypt
from termcolor import colored
import mysql.connector
import time
from prettytable import PrettyTable

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444@Root",
    database = "BankManagment"
)
mycursor = connection.cursor()

print(colored("╭─────────────────────────────────╮" , "magenta"))
print(colored("│     Welcome to MyBankBuddy      │", "magenta"))
print(colored("╰─────────────────────────────────╯" , "magenta"))

def signup():
    #<<------------------------------1nd-table(Customers)---------------------------------->>
    special_characters = "@._"

    #Username
    while True:
        try:
            username = input("Enter Username: ").strip()
            valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
            for c in username:
                if c not in valid_chars:
                    print(colored("Name must contain only letters.", "red"))
                    break  #it break for loop not while
            else:   
                break

        except ValueError:
            print(colored("Invalid username. Try again." , "red"))
            continue
    
    #Password
    while True:
        password = input("Enter Password to set: ")

        if len(password) < 6:
            print(colored("Password must be at least 6 or more characters." , "red"))
        elif not any(char.isupper() for char in password):
            print(colored("Password must contain at least one uppercase letter." , "red"))
        elif not any(char in special_characters for char in password):
            print(colored("Password must contain at least one special character like @, ., _," , "red"))
        else:
            salt = bcrypt.gensalt()
            key = bcrypt.hashpw(password.encode('utf-8'), salt)
            break 

    #Phone No.
    while True:
        phone = input("Enter Phone no: ")
        n = '789' 
        if len(phone) != 10 or not phone.isdigit():
            print(colored("Enter a valid 10-digit phone number.", "red"))
            continue
        if phone[0] not in n:
            print(colored("Indian numbers must start with 7, 8, or 9." , "red"))
            continue


        mycursor.execute("SELECT phone_number FROM Customers")
        myresult = mycursor.fetchall()
        phone_exist = False
        for result in myresult:
            if phone == result[0]: 
                phone_exist = True
                print(colored("Phone Number already used! Use another." , "red"))
                break 
            
        if phone_exist:
            continue  
        
        break
    
    #<<---------------------------Insert all in DB---------------------------------->>
    try:
        sql = "INSERT INTO Customers (Name, Password, phone_number) VALUES (%s, %s, %s)"
        mycursor.execute(sql, (username, key, phone))
        connection.commit()
    except mysql.connector.Error as e:
        print("Error:", e)
        connection.rollback()  
        
    #<<------------------------------2nd-table(Account)---------------------------------->>
    #Account type
    while True:
        print("What type of account would you like to open? ")
        print("╭─────────────────────────────────╮")
        print("│ 1] Savings Account.             │")
        print("│ 2] Current Account.             │")
        print("╰─────────────────────────────────╯")
        try:
            account_type = int(input("Enter Choice: "))
            
            if account_type == 1 or account_type == 2:
                a_type = "Savings Account" if account_type == 1 else "Current Account"
                
                sql2 = """
                INSERT INTO Accounts ( customer_id, account_type , phone_number )
                SELECT customer_id , %s , phone_number 
                FROM Customers
                WHERE phone_number = %s;
                """ 
                
                val = ( a_type , phone )
                mycursor.execute(sql2, val)
                
                if mycursor.rowcount > 0:
                    print("Account successfully created!")

                else:
                    print("Account creation failed. Please check the phone number.")
                connection.commit()
                break
                
            else:
                print("Invalid input enter only 1 or 2.")
                continue
                
        except:
            print(colored("Value Error! only 1 or 2 ", "red"))    
            continue

    #get customet_id from customer table   
    mycursor.execute("SELECT customer_id FROM Customers WHERE phone_number = %s" , (phone,))
    s1 = mycursor.fetchone()
    for i in s1:
        break
    
    #get account_id from account table
    mycursor.execute("SELECT account_id FROM Accounts WHERE customer_id = %s" , (i,))
    s2 = mycursor.fetchone()
    for j in s2:
        print("Printing Details....")
    
    #Time-Pass    
    time.sleep(2)    
    print(colored(f"Hey {username}, your account has been successfully created.","green"))
    print(colored("your account details are as follows: " , "green" )) 
    print(f"""╭─────────────────────────────────╮
  ➤ User_ID : {i}
  ➤ Account_ID : {j} 
  ➤ Account Type : {a_type}
  ➤ Name : {username}
  ➤ Password : {password}
  ➤ Mobile No : {phone}
╰─────────────────────────────────╯""" )
    print(colored("Note: " , "red") , end="")
    print("Remember your details. Your detail won't be shown again.")
    
    while True:
        i = str(input("Press \'N\' after reading the details: ")).lower()
        if i == "n":
            break
        else:
            print("Enter only \'N\' ")
            continue
        
# signup()

def login():
    while True:
        phone = input("Enter Your Phone no: ")

        mycursor.execute("SELECT Password FROM Customers WHERE phone_number = %s", (phone,))
        result = mycursor.fetchone()  # Fetch only one record

        if result:  # If a matching phone number is found
            hashed_password = result[0]  # Get the hashed password

            while True:
                password = input("Enter Your Password: ").encode()

                # Verify the password
                if bcrypt.checkpw(password, hashed_password.encode() if isinstance(hashed_password, str) else hashed_password):
                    print(colored("Login Successfully", "green"))
                    
                    print(colored("★  Welcome User!  ★ ", attrs=["bold"]))
                    print("Loading...")
                    
                    mycursor.execute("SELECT account_id FROM Accounts WHERE phone_number = %s " , (phone,))
                    b = mycursor.fetchone()
                    for acc_id in b:
                        print(f"Your Account ID is {acc_id}")
                        break
                            
                    time.sleep(2)
                    while True:
                        print("╭─────────────────────────────────╮")
                        print("│ 1] Check Balance.               │")
                        print("│ 2] Deposit Money.               │")
                        print("│ 3] Withdraw Money.              │")
                        print("│ 4] Transaction History.         │")
                        print("│ 5] Logout.                      │")
                        print("╰─────────────────────────────────╯")
                            
                        try:
                            choice2 = int(input("Enter your choice: "))
                            
                            if choice2 == 1:
                                mycursor.execute("SELECT Balance FROM Accounts WHERE account_id = %s " , (acc_id,))
                                w = mycursor.fetchone()
                                for balance in w:
                                    print("Your Bank Balance is: " , end="")
                                    print(colored(f"Rs.{balance}" , "green"))   
                                    break
                                continue
                            
                            if choice2 == 2:
                                
                                while True:
                                    try: 
                                        amount = int(input("Enter the amount to deposit: "))
                                        if amount <= 0 :
                                            print(colored("amount must be positive." , "red"))
                                            continue
                                        else:
                                            mycursor.execute("SELECT Balance FROM Accounts WHERE account_id = %s" , (acc_id,))
                                            myresult2 = mycursor.fetchone()
                                            for value in myresult2:
                                                value += amount
                                                break
                                            
                                            #1st query for account table
                                            sql1 = "UPDATE Accounts SET Balance = %s WHERE account_id = %s"
                                            val1 = ( value , acc_id )
                                            mycursor.execute(sql1,val1)
                                            connection.commit()
                                            
                                            print(f"Rs.{amount} Credited to A/c No. {acc_id} ")
                                                        
                                            #2nd table for transaction table
                                            sql2 = """
                                            INSERT INTO Transactions ( account_id , amount , type , BankBalance )
                                            SELECT account_id , %s , %s , %s
                                            FROM Accounts
                                            WHERE account_id = %s;
                                            """
                                            val = ( amount , "Credit" , value , acc_id )
                                            mycursor.execute(sql2 , val)
                                            
                                            if mycursor.rowcount > 0:
                                                print(colored("Money Credited" , "green"))
                                            else:
                                                print("Faild") 
                                                
                                            connection.commit()
                                            print("Now your account balance is: " , end='')
                                            print(colored(value , "green"))
                                            break 
                                        
                                    except:
                                        print(colored("ValueError! amount must be digits." , "red"))
                                        continue   
                                continue
                            
                            if choice2 == 3:
                                
                                while True:
                                    try: 
                                        amount = int(input("Enter the amount to withdraw: "))
                                        if amount <= 0 :
                                            print(colored("amount must be positive." , "red"))
                                            continue
                                        else:
                                            mycursor.execute("SELECT Balance FROM Accounts WHERE account_id = %s" , (acc_id,))
                                            myresult2 = mycursor.fetchone()
                                            for value1 in myresult2:
                                                if value1 < amount :
                                                    print(colored(f"Withdrawal of Rs.{amount} is not possible because your account balance is insufficient. Current balance: Rs.{value1}", "red"))
                                                    break
                                                
                                                if value1 <= 0:
                                                    print(colored(f"Account with ID {acc_id} has insufficient balance. Withdrawal not possible." , "red") )
                                                    break
                                                
                                                else:
                                                    value1 -= amount
                                                    #1st query for account table
                                                    sql3 = "UPDATE Accounts SET Balance = %s WHERE account_id = %s"
                                                    val3 = ( value1 , acc_id )
                                                    mycursor.execute(sql3,val3)
                                                    connection.commit()
                                            
                                                    print(f"Rs.{amount} Debited to A/c No. {acc_id} ")
                                                        
                                                    #2nd table for transaction table
                                                    sql4 = """
                                                    INSERT INTO Transactions ( account_id , amount , type , BankBalance )
                                                    SELECT account_id , %s , %s , %s
                                                    FROM Accounts
                                                    WHERE account_id = %s;
                                                    """
                                                    val4 = ( amount , "Debit" , value1 , acc_id )
                                                    mycursor.execute(sql4 , val4)
                                                    
                                                    if mycursor.rowcount > 0:
                                                        print(colored("Money Debited" , "green"))
                                                    else:
                                                        print("Faild") 
                                                        
                                                    connection.commit()
                                                    print("Now your account balance is: " , end='')
                                                    print(colored(value1 , "green"))
                                                    break
                                            break 
                                        
                                    except:
                                        print(colored("ValueError! amount must be digits." , "red"))
                                        continue   
                                    
                                continue
                                    
                            if choice2 == 4:
                                mycursor.execute("SELECT * FROM Transactions WHERE account_id = %s" , (acc_id,) )
                                myresult3 = mycursor.fetchall()
                                table = PrettyTable()
                                table.field_names = [ "Index" , "Transaction ID" , "Amount" , "Type" , "Date & Time" , "Balance" ]
                                
                                for index,transaction in enumerate(myresult3 , start=1) :
                                    transaction_id = transaction[0]
                                    amount = transaction[2]
                                    transaction_date = str(transaction[3])
                                    type = transaction[4]
                                    balance = transaction[5]
                                    table.add_row([index, transaction_id, amount, type, transaction_date, balance])
                                if mycursor.rowcount == 0 :
                                    print(f"No history available for user {acc_id}")    
                                    break
                                else:
                                    print("Transaction History:")
                                    print(table)
                                continue
                            
                            if choice2 == 5:
                                print(colored("Logout Succesfully.." , "green"))
                                break
                            else:
                                print(colored("Invalid Input!" , "red"))
                                continue 
                        except:
                            print(colored("ValueError! only numbers." , "red"))
                            continue

                    return  # Exit the function upon successful login

                else:
                    print(colored("Incorrect Password!", "red"))

        else:
            print(colored("User not found with this number.", "red"))
         
# login()

# Final Code ---------------------------------------------------------------------------

while True:

    print("╭─────────────────────────────────╮")
    print("│ 1] Create Account.              │")
    print("│ 2] Login.                       │")
    print("│ 3] Exit.                        │")
    print("╰─────────────────────────────────╯")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            signup()     #signup funciton
            continue
        elif choice == 2:
            login()      #login function
            continue
        elif choice == 3:
            print(colored("Thank you, come again" , "green" , attrs=["bold"]))
            break

    except:
        print(colored("ValueError! only numbers" , "red"))
        continue

    finally:
        connection.close()

