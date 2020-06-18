import random
import string

from .password import Password

class Passworify:
    '''Class to convert a string to a secure password
    
    Atributtes
    ----------
    string_to_password : str
        String to convert in a secure password
    password : Password
        Password instance that contains the password generated
    
    Methods
    _______
    parse()
        Converts the string to a Password object
    '''

    __vowels = {'a': '4', 'e': '3', 'i': '1', 'o': '0'}

    def __init__(self, string_to_password):
        self.string_to_password = string_to_password
        self.password = None

    def parse(self):
        tmp_password_string = self.string_to_password

        while not self.__is_strong_password_string(tmp_password_string):
            new_string = []

            for c in self.string_to_password:
                if c in string.whitespace:
                    new_string.append(random.choice(string.punctuation))
                elif c in string.ascii_lowercase and random.randint(0, 9) % 2 == 0:
                    new_string.append(c.upper())
                elif c in string.ascii_uppercase and random.randint(1, 3) % 2 == 0:
                    new_string.append(c.lower())
                elif c.lower() in Passworify.__vowels and random.randint(2, 4) % 2 == 0:
                    new_string.append(Passworify.__vowels[c.lower()])
                else:
                    new_string.append(c)
            
            tmp_password_string = ''.join(new_string)
        
        self.password = Password(password=tmp_password_string)

    def __is_strong_password_string(self, password_string):
        string_set = set(password_string)
        
        have_lowercase = string_set & set(string.ascii_lowercase)
        have_uppercase = string_set & set(string.ascii_uppercase)
        have_digit = string_set & set(string.digits)
        have_punctuation = string_set & set(string.punctuation)

        return have_lowercase and have_uppercase and have_digit and have_punctuation
