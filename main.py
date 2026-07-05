# main function
from login import *

def main():
    running = True
    print("Welcome to Password Manager!")
    while running:
        print("\n=== MAIN MENU ===")
        print("1. Register username")
        print("2. Login with existing user")
        print("3. Exit")
        choise = input("Enter your choise (1-3):")
        match choise:
            case '1':
                while True:
                    user=input("Input username:")
                    if verify_user(user) == False:
                        print(f"Hi {user}, please enter your password.")
                        register_password=input("Enter user password:")
                        register_user(user,register_password)
                    else:
                        print("This user already exists! Please enter a non existing username or exit.")
                        print("1. Enter another username for register.")
                        print("2. Back to Main Menu")
                        choise_1=input("Enter your choise (1-2):")
                        if choise_1 != '1':
                            break

            case '2':
                while True:
                    user=input("\nInput username:")
                    if verify_user(user) == False:
                        print("\nIncorrect username or password!")
                        print("1. Try again")
                        print("2. Back to Main Menu")
                        choise_2=input("Enter your choise (1-2):")
                        if choise_2 != '1':
                            break
                    else:
                        while True:
                            password=input("Enter password:")
                            if verify_login(user,password) == True:
                                print(f"Login successful! Welcome back, {user}.")
                                in_safe=True
                                while in_safe:
                                    print(f"\n --- {user.upper()}'S PASSWORD MANAGER --- ")
                                    print("1. View saved password")
                                    print("2. Add new password")
                                    print("3. Log out")
                                    safe_option=input("chose an option (1-3):")

                                    match safe_option:
                                        case '1':
                                            print_safe(user)
                                        case '2':
                                            site=input("Enter website/app name:")
                                            site_user=input("Enter username/email for this site:")
                                            site_pass=input("Enter password for this site:")
                                            add_password_safe(user,site,site_user,site_pass)
                                        case '3':
                                            print("Logging out...")
                                            in_safe=False
                                running = False
                                break
                            else:
                                print("Incorrect username or password!")
                                print("1. Try again.")
                                print("2. Back to Main Menu")
                                choise_3=input("Enter your choise (1-2):")
                                if choise_3 !='1':
                                    break
                        break
                            
            case '3':
                running=False
            case _:
                print("Incorrect choise! Please enter a valid choise")
                



if __name__ == '__main__':
    main()