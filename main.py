import csv
import os
import stat
from cryptography.fernet import Fernet


KEY_FILE = 'ferney_key.key'


def generate_or_load_key():
    '''Generate or load encryption key.

    This function generates a new encryption key if the key file doesn't exist,
    or loads the existing key from the file. It ensures the key file has the appropriate permissions.'''

    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, 'rb') as key_file:
                key = key_file.read()
        except FileNotFoundError:
            print("KEY_FILE not found.")
        except PermissionError:
            print('Permission error accessing the password manager.')
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)

    os.chmod(KEY_FILE, stat.S_IRWXU)

    return key


key = generate_or_load_key()
encryptor = Fernet(key)


def encrypt(message: bytes):
    '''Encrypt a message using Fernet encryption.

    This function takes a message in bytes format and encrypts it using a pre-generated
    Fernet encryption key. The encrypted message is returned.'''

    encrypted_message = encryptor.encrypt(message)
    return encrypted_message


def decrypt(encrypted_message: bytes):
    '''Decrypt an encrypted message.

    This function decrypts an encrypted message provided in bytes format using the
    Fernet encryption key. The decrypted message is returned as a string.'''

    decrypted_message = encryptor.decrypt(
        encrypted_message).decode('utf-8')
    return decrypted_message


def store_master_pw(master_pw: bytes):
    '''Encrypt and store the master password. 

    This function takes the master password in bytes format, encrypts it using the
    Fernet encryption key, and stores the encrypted password in a binary file named 'bin.txt'.'''

    encrypted_master_pw = encrypt(master_pw)
    with open('bin.txt', 'wb') as f:
        f.write(encrypted_master_pw)


def verify_master_pw():
    '''verify if the master password entered by the user matches the master password stored'''

    master_pw = input("Enter your Master Password: ")

    try:
        with open('bin.txt', 'rb') as myfile:
            encrypted_master_password = myfile.read()
    except FileNotFoundError:
        print('Master Password file not found.')
    except PermissionError:
        print('Permission error accessing the password manager.')

    decrypted_master_pw = decrypt(encrypted_master_password)
    if master_pw == decrypted_master_pw:
        return True
    else:
        return False


def create_password_manager(fieldnames: list):
    '''Create a new password manager file with specified fieldnames.'''

    with open('password manager.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    os.chmod('password manager.csv', stat.S_IRWXU)


def check_password_manager(fieldnames: list):
    '''Check if a password manager file exists and create one if not.'''

    password_manager_exists = "password manager.csv" in os.listdir(os.getcwd())
    if password_manager_exists == False:
        create_password_manager(fieldnames=fieldnames)
        print("There's no existing Password Manager. Let's create one!")
        print("Enter a Master Password")
        master_password = input('> ').encode('utf-8')
        store_master_pw(master_password)


def update_password_manager(title: str, website: str, username: str, password: str, notes: str, fieldnames: list):
    '''Add a new row to the password manager CSV file'''
    # Create a dictionary for the new entry
    data_dict = {'Title': title, 'Website/App': website,
                 'Username': username, 'Password': password, 'Notes': notes}

    # Open the CSV file in append mode and write the new entry
    try:
        with open('password manager.csv', mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(data_dict)
    except FileNotFoundError:
        print('Password Manager not found.')
    except PermissionError:
        print('Permission error accessing the password manager.')


def view_password(credential_title: str):
    '''View details of an existing password entry based on its title.'''

    try:
        with open('password manager.csv', mode='r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            # Iterate through each row in the CSV file
            for row in reader:
                # Check if the title of the current row matches the provided credential title
                if row['Title'] == credential_title:
                    # Retrieve credential details from csv_file
                    title, password, website, username, notes = row['Title'], row[
                        'Password'], row['Website/App'], row['Username'], row['Notes']
                    decrypted_password = decrypt(password.encode('utf-8'))

                    # Print out the credential details
                    print(f'Title: {title}')
                    print(f'Password: {decrypted_password}')
                    print(f'Website/App: {website}')
                    print(f'Username: {username}')
                    print(f'Notes: {notes}')
                    return
    except FileNotFoundError:
        print('Password Manager not found.')
    except PermissionError:
        print('Permission error accessing the password manager.')

    print(f'No password stored for {credential_title}.')


def get_new_credential():
    '''Prompt the user to enter a new credential to add to the password manager.'''

    # Initialize an empty dictionary to store the new credential details
    new_credential = {}
    # Prompt the user to input the details  of the new credential
    new_credential['title'] = input('Title: ').capitalize()
    new_credential['website'] = input('Website/App: ')
    new_credential['username'] = input('Username: ')
    password = input('Password: ').encode('utf-8')
    # Encrypt the password using the encrypt function
    encrypted_password = encrypt(password)
    new_credential['password'] = encrypted_password.decode('utf-8')
    new_credential['notes'] = input('Notes: ')

    return new_credential


def main():
    fieldnames = ['Title', 'Website/App', 'Username', 'Password', 'Notes']

    # Check if the Password Manager already exists. If not, create one.
    check_password_manager(fieldnames)

    # Prompt user to enter master password and verify it.
    verified_master_pw = verify_master_pw()
    if verified_master_pw:
        # Choose mode: Add or View password
        print('Would you like to "Add" or "View" password?')
        pm_mode = input('> ').lower()
        if pm_mode == 'add':
            add_new_credential = True
            while add_new_credential:
                new_credential_dict = get_new_credential()
                update_password_manager(
                    **new_credential_dict, fieldnames=fieldnames)
                print('Add more? "Y" or "N". ')
                add_new_credential = 'Y' == input('> ').upper()

        elif pm_mode == 'view':
            title = input('Enter the "Title" of the credential: ').capitalize()
            view_password(title)
        else:
            print('Invalid mode.')
    else:
        print('Wrong Master Password.')


if __name__ == '__main__':
    main()
