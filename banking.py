# Creation of a table
import sqlite3
conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
QUERY = '''CREATE TABLE card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );'''
# cur.execute(QUERY)
# After making some changes in DB don't forget to commit them!
conn.commit()


###########################################################

import random

# Luhn function
def luhn_alg(number_cardx):
    int_number_cardx = list(map(int, list(number_cardx)))

    for n in range(len(int_number_cardx)):
        if (n+1) % 2 != 0:
            int_number_cardx[n] *= 2

        if int_number_cardx[n] > 9:
            int_number_cardx[n] -= 9

    l_digit = (10 - sum(int_number_cardx) % 10) % 10
    return l_digit

# Validation Luhn
def luhn_alg_validate(number_cardxo):
    int_number_cardxo = list(map(int, list(number_cardxo)))
    int_number_cardx = int_number_cardxo[:-1]
    for n in range(len(int_number_cardx)):
        if (n+1) % 2 != 0:
            int_number_cardx[n] *= 2

        if int_number_cardx[n] > 9:
            int_number_cardx[n] -= 9

    l_digit = (int_number_cardxo[-1] + sum(int_number_cardx)) % 10
    return (0 if l_digit == 0 else 1)

# OOP
class CreditCard:

    def __init__(self):
        pass
    
    # Method to create the number and Pin of a card with the Luhn function
    def create_card(self):
        while True:
            random.seed()
            pin = format(random.randint(0, 9999), "04")
            number_card_prev = "400000" + format(random.randint(0, 999999999), "09")
            # We use the Luhn function to define the last digit
            last_digit = luhn_alg(number_card_prev)
            number_card = number_card_prev + str(last_digit)
            # We check if the card created already exists
            cur.execute(f"SELECT number, pin FROM card WHERE number={number_card} AND pin={pin};")
            variable = cur.fetchall()
            
            # If the card doesnt exists then we continue
            if len(variable) != 0:
                continue
            else:
                cur.execute(f'INSERT INTO card (number, pin) VALUES ({number_card}, {pin});')
                # After making some changes in DB don't forget to commit them!
                conn.commit()
                break

        print("Your card has been created", "Your card number:", sep="\n")
        print(number_card)
        print("Your card PIN:")
        print(pin)
    
    # Method to login in our account
    def login(self, number_card, pin):

        cur.execute(f"SELECT number FROM card WHERE number={number_card} AND pin={pin};")
        num_a = cur.fetchone()
        
        # if the card exists
        if num_a is not None:
            print("You have successfully logged in!")

            # We go in the options of our account
            while True:
                print("1. Balance", "2. Add income", "3. Do transfer", "4. Close account", "5. Log out", "0. Exit", sep="\n")
                number_s = int(input())
                
                # Check the balance
                if number_s == 1:
                    cur.execute(f"SELECT balance FROM card WHERE number={number_card} AND pin={pin};")
                    balance = cur.fetchone()
                    print(f"Balance: {balance}")
                    
                # Add income    
                elif number_s == 2:
                    print("Enter income")
                    income = int(input())
                    # Check our actual income and extract the value
                    cur.execute(f"SELECT balance FROM card WHERE number={number_card} AND pin={pin};")
                    balance_a = cur.fetchone()
                    # Sum the actual balance with the income and put into the database
                    new_balance_a = balance_a[0] + income
                    cur.execute(f'UPDATE card SET balance={new_balance_a} WHERE number={number_card};')
                    conn.commit()
                    print("Income was added!")
                    
                # Do transfer    
                elif number_s == 3:
                    print("Transfer", "Enter card number:", sep="\n")
                    card_to_transfer = input()
                    cur.execute(f"SELECT number FROM card WHERE number={card_to_transfer};")
                    num_b = cur.fetchone()
                    
                    # we check if the card to transfer is using the Luhn function
                    if luhn_alg_validate(card_to_transfer) != 0:
                        print("Probably you made a mistake in the card number. Please try again!")
                    # if the card is not found in the database    
                    elif num_b is None:
                        print("Such a card does not exist.")
                    # if the card to transfer is equal to our card    
                    elif card_to_transfer == number_card:
                        print("You can't transfer money to the same account!")
                    # if the card is found in the database    
                    elif num_b is not None:
                        # We extract the balance of the two cards and select the money that we want to transfer
                        print("Enter how much money you want to transfer:")
                        money = int(input())
                        cur.execute(f"SELECT balance FROM card WHERE number={card_to_transfer};")
                        balance_b = cur.fetchone()
                        cur.execute(f"SELECT balance FROM card WHERE number={number_card};")
                        balance_a = cur.fetchone()
                        
                        # if the money that we want to transfer is higher than the money that we have in our balance
                        if money > balance_a[0]:
                            print("Not enough money!")
                        else:
                            money_transfer = balance_b[0] + money
                            cur.execute(f'UPDATE card SET balance={money_transfer} WHERE number={card_to_transfer};')                # After making some changes in DB don't forget to commit them!
                            conn.commit()
                            cur.execute(f'UPDATE card SET balance={balance_a[0] - money} WHERE number={number_card};')                # After making some changes in DB don't forget to commit them!
                            conn.commit()
                            print("Success!")

                # Close account, it means delete it
                elif number_s == 4:
                    cur.execute(f'DELETE FROM card WHERE number = {number_card}')
                    conn.commit()
                    print("The account has been closed!")
                    break
                
                # Exit
                elif number_s == 0:
                    global number
                    number = 0
                    break # break to finish the while
                    
                # if the number selected is not in the options    
                else:
                    print("use a correct number please")
       
    # if the card doesnt exists
        else:
            print("wrong")

############################################################################################################

# main code
while True:

    print("1. Create an account", "2. Log into account", "0. Exit", sep="\n")
    number = int(input())

    # Options if we select a number
    if number == 1:
        user_card = CreditCard()
        user_card.create_card()

    elif number == 2:
        print("Enter your card number:")
        number_card = input()
        print("Enter your PIN:")
        pin = input()
        user_card = CreditCard()
        user_card.login(number_card, pin)

        if number == 0:  # Exit too
            print("Bye!")
            break

    elif number == 0:  # Exit
        print("Bye!")
        break

    else:
        print("Enter a correct number please")
