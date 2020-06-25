from cryptography.fernet import Fernet
import filecmp
import shutil
import tempfile
import argparse

# ---------------------------------------------------------------------
#                           Key Creation
# ---------------------------------------------------------------------
def create_key(path):
    '''

    This function creates a key to encrypt and 
    decrypt files. Keep this key safely. If you 
    lose this key, your file containing your 
    passwords is lost forever!

    path (click.File): An opened file that we can write to.

    returns: True

    creates: A file that contains the key for later use.

    '''

    key = Fernet.generate_key()

    path.write(key)

    return True
     
# ---------------------------------------------------------------------
#                        New Passwords Files
# ---------------------------------------------------------------------
def create_password(passwords, key, newfile):
    '''
    This functions encrypts every passwords in the provided list using 
    the provided key. It then writes the passwords to newfile.

    passwords (list of strings): A list of unencrypted passwords.

    key (str): The Fernet key that will be used to encrypt the 
    passwords.

    newfile (click.File): An opened file that we can write to.
    '''
    f = Fernet(key)
    for password in passwords:
        encoded = password.encode('utf-8')
        encrypted = f.encrypt(encoded)
        newline = '\n'.encode('utf-8')
        text = encrypted + newline
        newfile.write(text)

    return newfile.name

# ---------------------------------------------------------------------
#                   Adding To Existing Password File
# ---------------------------------------------------------------------

def adder(password, key, existing_file, position):
    '''
    This function encrypts password using key. It then adds password to
    existing file at the provided position.

    password (str): The password to add.

    key (str): A Fernet key (The one that was used to create the 
    file).

    existing_file (click.File): An opened file that we can write to.

    position (int): Where to write the new password assuming that the 
    existing passwords are in a list splitted on newlines.

    returns (str): P
    '''
    f = Fernet(key)
    lines = existing_file.readlines()

    # Encrypting the password.
    encoded = password.encode('utf-8')
    encrypted = f.encrypt(encoded)
    newline = '\n'.encode('utf-8')
    to_add = encrypted + newline

    # Adding the password to the list.
    lines[position:position] = [to_add]
    
    # Creating temporary file and writing to it.
    x = tempfile.NamedTemporaryFile(mode = 'w+b', delete = False)
    x.writelines(lines)
    x.close()

    # Copying the file to the new file
    shutil.move(x.name, existing_file.name) 
    
    return existing_file.name
