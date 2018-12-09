def sign_up():
    username = raw_input('Enter Username: ')

    while True:
        password = raw_input('Enter Password: ')
        password2 = raw_input('Confirm Password: ')

        if password == password2:
            # TODO send info to server and ensure username is unique
            return username
        else:
            print('Password did not match confirmation. Please re-enter password')

# This function allows the user to enter a username and password which will be verified by the
def user_login():
    username = raw_input('Enter Username: ')
    password = raw_input('Enter Password: ')
    #TODO send info to server and check validity

# This function will print options for the user to sign in or create an account. The function will
# send the user info to the server and give the user more options after successful login or account creation
def login_page():
    print('1. Sign up')
    print('2. Login')
    print('3. Exit')

    while True:
        user_input = raw_input()

        if user_input == '1':
            #create new account
            return sign_up()

        elif user_input == '2':
            #login to account
            return user_login()

        elif user_input == '3':
            #exit program
            return

        else:
            #user input was not a usable value
            print('Invalid Entry. Please try again')



# This is the main function where other helper functions will be called
def main():
    print('Welcome to AB Conversation! What would you like to do?')
    username = login_page()




# this is where the code is initiated
main()

#print farewell statement after logging out of the app
print('Goodbye!')