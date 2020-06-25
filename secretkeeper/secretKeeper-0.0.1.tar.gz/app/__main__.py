import click
from funcmodule import *

@click.group()
def main():
    '''
    This is a short encryption tool that can be used to 
    generate Fernet encryption keys and encrypt passwords.
    '''
    pass

# ---------------------------------------------------------------------
#                           Key Creation
# ---------------------------------------------------------------------

# Creating a new command.
@click.command()

# Adding possible arguments.
@click.argument(
        'output', 
        type = click.File('wb')
        )
def keygen(output):
    '''
    Generates a Fernet key and writes the key to the
    specified output file.
    '''
    create_key(output)
    message = '''\
            Your fernet key has been written under %s. Keep it safe!
            '''%(output.name)
    click.echo(message)
    
    return None

# ---------------------------------------------------------------------
#                        New Passwords Files
# ---------------------------------------------------------------------

# Creating a new command.
@click.command()

# Adding possible arguments.
@click.argument(
        'output',
        type = click.File('wb')
        )
@click.argument(
        'key',
        type=click.File('rb')
        )
@click.option(
        '-n',
        '--number', 
        default=1, 
        show_default = True, 
        type = int,
        help = '''\
                The number of passwords you want to write to the file.
                '''
        )
def new_passwords(output, key, number):
    '''
    Encrypt passwords provided by the user using a provided key. The 
    encrypted passwords are then written to a new file.
    '''
    passwords = []
    for i in range(number):
        to_prompt = 'Password #%s'%(i+1)
        passwords.append(click.prompt(to_prompt, hide_input = True))

    key_name = key.name
    key = key.read()

    name = create_password(passwords, key, output)

    message = '''\
            Your passwords have been saved in %s using %s.
            '''%(name, key_name)

    click.echo(message)
    return None
# ---------------------------------------------------------------------
#                   Adding To Existing Password File
# ---------------------------------------------------------------------

# Creating a new command.
@click.command()

# Adding possible arguments.
@click.argument(
        'existing_file',
        type = click.File('rb')
        )
@click.argument(
        'key',
        type = click.File('rb')
        )
@click.option(
        '-p',
        '--position',
        default = -1,
        show_default = True,
        type = int,
        help = '''\
                Assuming your passwords are stored as a list, this is 
                the index where the new password will be added.'''
        )
def add_password(existing_file, key, position):
    '''
    Adds a new password to the provided file. If a position is 
    provided, the password will be inserted at this index. If password 
    0,1,2,3, and new password is inserted at index = 2, password 2 
    becomes password 3, and 3 becomes password 4.
    '''
    key = key.read() 

    new_password =  click.prompt('New password', hide_input = True)

    location = adder(new_password, key, existing_file, position)

    message = '''\
            Your password has been saved in %s at position %s.
            '''%(location, position)
    
    click.echo(message)

    return None
     

# Adding the commands to the main click object.
main.add_command(add_password)
main.add_command(keygen)
main.add_command(new_passwords)

if __name__ == '__main__':
    main()
