
import pyperclip


def copy(text):
    pyperclip.copy(text)
    return True


def paste():
    text = pyperclip.paste()
    return text

