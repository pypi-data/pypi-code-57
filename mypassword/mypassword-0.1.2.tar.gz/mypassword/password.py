import random
import string

class PasswordLevel:
    '''Class to define the levels of security for a password
    
    There are four levels:
    ONE
    TWO
    THREE
    FOUR
    '''

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


class Password:
    '''Class to representate a password
    
    Atributtes
    ----------
    level : int, optional
        The password security level. You can use a constant from PasswordLevel. (Default is PasswordLevel.ONE)
    length : int, optional
        The length of the password. (Default is 8)
    password: str, optional
        The password string. You can generate one or use an existing one. (Defualt is None)
        If you don't pass the param, a random password will be created.
    '''

    def __init__(self, length=8, level=PasswordLevel.ONE, password=None):
        if password:
            self.__verify_invalid_chars(password)
            self.level, self.length, self.password = self.__identify_password(password)
        else:
            self.length = length
            self.level = level
            self.password = self.__get_random_string()

    def __str__(self):
        return f'{self.password}'

    def __get_random_string(self):
        random_string = []
        available_levels = self.__get_available_levels()

        if self.length < 8:
            raise Exception('The length cannot be less than 8')
        
        random_string = [self.__get_level_char(i) for i in available_levels]
        random.shuffle(random_string)

        for i in range(self.length - self.level):
            next_char_level = random.choice(available_levels)
            random_string.append(self.__get_level_char(next_char_level))

        return ''.join(random_string)

    def __get_level_one_char(self):
        return random.choice(string.ascii_lowercase)

    def __get_level_two_char(self):
        return random.choice(string.ascii_uppercase)

    def __get_level_three_char(self):
        return random.choice(string.digits)

    def __get_level_four_char(self):
        return random.choice(string.punctuation)

    def __get_level_char(self, level):
        char = ''

        if level == PasswordLevel.ONE:
            char = self.__get_level_one_char()
        elif level == PasswordLevel.TWO:
            char = self.__get_level_two_char()
        elif level == PasswordLevel.THREE:
            char = self.__get_level_three_char()
        elif level == PasswordLevel.FOUR:
            char = self.__get_level_four_char()
        else:
            raise Exception(f'The level {level} does not exists')
        
        return char

    def __get_available_levels(self):
        levels = []

        for i in range(self.level, PasswordLevel.ONE - 1, -1):
            if i == PasswordLevel.ONE:
                levels.append(PasswordLevel.ONE)
            elif i == PasswordLevel.TWO:
                levels.append(PasswordLevel.TWO)
            elif i == PasswordLevel.THREE:
                levels.append(PasswordLevel.THREE)
            elif i == PasswordLevel.FOUR:
                levels.append(PasswordLevel.FOUR)
            else:
                raise Exception(f'The level {i} does not exists')
        
        return list(set(levels))

    def __verify_invalid_chars(self, password):
        password_set = set(password)

        if password_set & set(string.whitespace):
            raise Exception('The password contains illegal characters')

    def __identify_password(self, password):
        level = 0
        length = len(password)
        
        password_set = set(password)
        results = [
            password_set & set(string.ascii_lowercase),
            password_set & set(string.ascii_uppercase),
            password_set & set(string.digits),
            password_set & set(string.punctuation)
        ]

        for result in results:
            if result:
                level += 1
        
        return level, length, password