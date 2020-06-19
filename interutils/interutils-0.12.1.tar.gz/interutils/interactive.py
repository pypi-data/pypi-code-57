from termcolor import colored, cprint


def clear() -> None:
    """
    Clear the screen by sending an escape sequence
    """
    print(chr(27) + "[2J")


def cyan(text: str) -> str:
    """
    Color a string in cyan
    """
    return colored(text, 'cyan')


def pr(text: str, notation='+', end='\n') -> None:
    """
    Fancy print function
    Adds a colored bracket-wrapped sign in front of the text
    * Default sign is '+'
    """
    col = {
        '+': 'green',
        '*': 'cyan',
        '~': 'cyan',
        'X': 'red',
        '!': 'yellow',
        '?': 'blue'
    }[notation]
    print(f"{colored(f'[{notation}]' , col)} {text}", end=end)


def choose(options: iter = ('Yes', 'No'), prompt: str = 'Choose action:', default: int = 0) -> int:
    """
    Presents a list of options to the user,
        allowing him to numerically select a desired one.

    * Returns: The selected item's index
    * Returns: -2 => KeyboardInterrupt caught
    * Returns: -1 => Bad input received
    """
    if not options:
        raise ValueError(
            " [!] No options passed to choice() !!!")  # No options
    pr(prompt, '?')
    for index, option in enumerate(options):
        line = '\t'
        if index == default:
            line += '[%d]. ' % (index + 1)
        else:
            line += ' %d.  ' % (index + 1)
        line += option
        cprint(line, 'yellow')
    try:
        ans = input(colored('[>>>] ', 'yellow'))
        if not ans:
            return default
        ans = int(ans)
        assert 0 < ans <= len(options)
        return ans - 1
    except KeyboardInterrupt:
        return -2  # Keyboard Interrupt
    except AssertionError:
        return -1  # Bad Number
    except ValueError:
        return -1  # Probably text received


def ask(question: str) -> (None, str, int):
    """
    Ask the user something by giving him a question

    * Returns: The response as int if possible
        otherwise as str, None if no response
    * Expect: KeyboardInterrupt
    """
    pr(question, '?')
    answer = input('>')
    if answer == '':
        return None
    try:
        answer = int(answer)
    except ValueError:
        pass
    return answer


def pause(reason: str = 'continue', cancel: bool = False) -> bool:
    """
    Show a message and wait for an enter key to be pressed

    Returns: True after [ENTER] pressed
    Returns: False after [^C] pressed
    """
    s = 'Press %s to %s' % (colored('[ENTER]', 'cyan'), reason)
    if cancel:
        s += ', %s to cancel' % colored('[^C]', 'red')
    pr(s, '?')

    try:
        input()
        return True
    except KeyboardInterrupt:
        return False


def banner(txt: str, style: str = 'slant') -> str:
    """
    A static wrapper around pyfiglet that allows easy creation of figlets

    Requires: "pyfiglet"
    Param: style: The style (From: /usr/lib/python*/site-packages/pyfiglet/fonts/)
    Returns: The created ASCII art
    """
    try:
        from pyfiglet import Figlet
    except ImportError:
        pr('Module "pyfiglet" not installed, rendering legacy banner', '!')
        return '~=~=~ %s ~=~=~' % txt
    f = Figlet(font=style)
    return f.renderText(text=txt)


def get_date() -> str:
    """
    Returns: Today's date (e.g. "28.11.2017" ;P)
    """
    from datetime import datetime
    return datetime.now().strftime("%d.%m.%Y")
