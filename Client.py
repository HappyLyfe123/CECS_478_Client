import requests
import encrypter, decrypter
import json
import os

# This is the main function where other helper functions will be called
def main():
    connection_response = requests.get('https://abconversation.us/')

    if connection_response.status_code == 502:
        print('Trouble connecting to server. Please try again later.')
        return

    print(json.loads(connection_response.text)['message'])

    print('What would you like to do?')
    username, jwt = login_page()

    # exit function if user chose to exit
    if username == None:
        return

    print("Welcome " + username + ". What would you like to do?")
    print('1. Send a message')
    print('2. Check for new messages')
    print('3. Logout')

    while True:
        user_input = raw_input()

        if user_input == '1':
            # Start a new conversation
            sendMessage(username, jwt)

        elif user_input == '2':
            # Enter a conversation with a friend that is already connected
            return

        elif user_input == '3':
            # exit program
            return

        else:
            #user input was not a usable value
            print('Invalid Entry. Please try again')



def sign_up():
    username = raw_input('Enter Username: ')

    while True:
        password = raw_input('Enter Password: ')
        password2 = raw_input('Confirm Password: ')

        # make sure password was entered the same way twice
        if password == password2:
            response = requests.post('https://abconversation.us/signup', data = {'username': username, 'password': password}).json()

            if 'message' in response:
                # server created the new user
                print(response.get('message'))
                jwt = response.get('jwt')
                return username, jwt
            else:
                # server returned an error and did not create the new user
                print('Username not available. Please choose a different username')
                username = raw_input('Enter Username: ')

        else:
            print('Password did not match confirmation. Please re-enter password')



# This function allows the user to enter a username and password which will be verified by the
def user_login():
    while True:
        username = raw_input('Enter Username: ')

        # allow user to exit program
        if username == 'EXIT!':
            return None, None

        password = raw_input('Enter Password: ')

        # allow user to exit program
        if password == 'EXIT!':
            return None, None

        response = requests.get('https://abconversation.us/login', headers={'username': username, 'password': password}).json()

        try:
            if 'jwt' in response:
                return username, response.get('jwt')
        except TypeError:
            #jwt was not returned so the username or password was incorrect
            print("Incorrect Username or Password. Please try again or enter EXIT! to exit")



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
            return None, None

        else:
            #user input was not a usable value
            print('Invalid Entry. Please try again')


def sendMessage(username, jwt):
    print('Who would you like to send your message to?')

    # check key folder for users who have shared their public keys
    keys = os.listdir('keys')

    users = {'test.pem', 'also test.pem'}

    for k in keys:
        if k != 'public.pem' and k != 'private.pem':
            # add username to set and remove filetype
            users.add(k.replace('.pem', ''))

    if len(users) == 0:
        #no eligible users so return to main menu
        print('No eligible users. Please put a users public key (ex. bob.pem) in the keys folder to send a message')
        return

    #print all eligible users with a number by their name
    count = 1
    for u in users:
        print(str(count) + '. ' + u)
        count += 1


def receiveMessage(username, jwt):
    response = requests.get('https://abconversation.us/message', headers={'Authorization': jwt}).json()
    print(response)

# this is where the code is initiated
main()

#print farewell statement after logging out of the app
print('Goodbye!')