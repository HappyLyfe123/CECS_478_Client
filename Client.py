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
    username, jwt, password = login_page()

    # exit function if user chose to exit
    if username == None:
        return

    print("Welcome " + username + ". \n")

    while True:
        print("What would you like to do?")
        print('1. Send a message')
        print('2. Check for new messages')
        print('3. Logout')

        user_input = input()

        if user_input == '1':
            # Start a new conversation
            sendMessage(username, jwt)

        elif user_input == '2':
            # check to see if you've received messages from friends
            receiveMessage(username, jwt, password)

        elif user_input == '3':
            # exit program
            return

        else:
            #user input was not a usable value
            print('Invalid Entry. Please try again')



def sign_up():
    username = input('Enter Username: ')

    while True:
        password = input('Enter Password: ')
        password2 = input('Confirm Password: ')

        # make sure password was entered the same way twice
        if password == password2:
            response = requests.post('https://abconversation.us/signup', data = {'username': username, 'password': password}).json()

            if 'message' in response:
                # server created the new user
                print(response.get('message'))
                jwt = response.get('jwt')
                return username, jwt, password
            else:
                # server returned an error and did not create the new user
                print('Username not available. Please choose a different username or type EXIT to leave')
                username = input('Enter Username: ')
                if username == 'EXIT':
                    return None, None, None

        else:
            print('Password did not match confirmation. Please re-enter password')



# This function allows the user to enter a username and password which will be verified by the
def user_login():
    while True:
        username = input('Enter Username: ')

        # allow user to exit program
        if username == 'EXIT!':
            return None, None, None

        password = input('Enter Password: ')

        # allow user to exit program
        if password == 'EXIT!':
            return None, None, None

        response = requests.get('https://abconversation.us/login', headers={'username': username, 'password': password}).json()

        try:
            if 'jwt' in response:
                return username, response.get('jwt'), password
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
        user_input = input()

        if user_input == '1':
            #create new account
            return sign_up()

        elif user_input == '2':
            #login to account
            return user_login()

        elif user_input == '3':
            #exit program
            return None, None, None

        else:
            #user input was not a usable value
            print('Invalid Entry. Please try again')


def sendMessage(username, jwt):
    print('Who would you like to send your message to?')

    # check key folder for users who have shared their public keys
    keys = os.listdir('keys')

    users = []

    for k in keys:
        if not k.__contains__(username) and k.__contains__('_public.pem'):
            # add username to set and remove filetype
            users.append(k.replace('_public.pem', ''))

    if len(users) == 0:
        #no eligible users so return to main menu
        print('No eligible users. Please put a users public key (ex. bob_public.pem) in the keys folder to send a message')
        return

    #print all eligible users with a number by their name

    for i in range(len(users)):
        print(str(i + 1) + '. ' + users[i])

    choice = None

    try:
        choice = int(input())
    except ValueError:
        #reject if input is not an integer
        print('Invalid value. Returning to menu \n')
        return

    # decrement choice because indexes are zero based
    choice -= 1

    if choice < 0 or choice >= len(users):
        #reject if integer is not in range
        print('Invalid value. Returning to menu \n')
        return

    #get public key path of chosen user
    keypath = 'keys/' + users[choice] + '_public.pem'

    message = input('Message to send to ' + users[choice] + ': ')

    #encrypt message to prepare for sending
    encrypted_message = encrypter.encrypt_message(message, keypath)

    response = requests.post('https://abconversation.us/message', headers={'Authorization': jwt}, data={'message': json.dumps(encrypted_message), 'id' : username,'receiverUsername' : users[choice]}).json()

    if 'Respond Message' in response:
        print(response.get('Respond Message'))
    else:
        print(response.get('Error Message'))



def receiveMessage(username, jwt, password):
    response = requests.get('https://abconversation.us/message', headers={'Authorization': jwt}, data={'id' : username}).json()

    if len(response) == 0:
        print('\nNo New Messages\n')
        return
    else:
        print('\nMessages:')

    for message in response:

        # get private key path of user
        keypath = './keys/' + username + '_private.pem'

        # decrypt message
        decrypted_message = decrypter.decrypt_message(json.loads(message["message"]), keypath, password)

        # print message with sender name next to it
        print(message.get('senderUsername') + ': ' + decrypted_message + '\n')

        messageID = message.get('_id')

        #delete message from server
        requests.delete('https://abconversation.us/message', headers={'id': messageID})

# this is where the code is initiated
main()

#print farewell statement after logging out of the app
print('Goodbye!')