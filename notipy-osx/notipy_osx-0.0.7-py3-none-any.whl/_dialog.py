import os
import subprocess

from notipy_osx._result import Result


def dialog_prompt(text, default_answer=None, buttons=["Cancel", "Continue"], default_button=None, cancel_button=None, icon=None, password=False):
  buttons_string = ""
  for button in buttons:
    buttons_string += f'"{button}",'
  buttons_string = buttons_string[:-1]  # remove the last trailing comma

  applescript = f'''\
  display dialog "{text}" buttons {{ {buttons_string} }} \
  '''

  # if default buttons not provided, set them manually
  # only set cancel button default is buttons list len more than 1
  if cancel_button:
    applescript += f'cancel button "{cancel_button}" '
  if default_button:
    applescript += f'default button "{default_button}" '

  if icon:
    if '.' in icon:
      # get current working directory
      pwd = subprocess.check_output('pwd', shell=True)
      pwd = pwd.decode('utf-8').rstrip()  # convert to strng and remove trailing neewlines
      icon_dir = f'{pwd}/{icon}'
      applescript += f'with icon POSIX file "{icon_dir}" '
    else:
      # if there's not file extension in the icon, it's an apple script default provided icon
      applescript += f'with icon {icon} '

  # only if default answer is set, show the text field
  if default_answer is not None:
    applescript += f'default answer "{default_answer}" '

    # the password field won't be there if there is no text field
    if password:
      applescript += f"with hidden answer "

  # osascript -e ... runs an applescript in the terminal
  command = f"""
    osascript -e '\
      set answer to {applescript} 
      return answer
    '
  """

  try:
    # run the terminal command and get the output
    result = subprocess.check_output(command, shell=True)
    result_string = result.decode('utf-8')
  except:
    # if there's an error, it means that the user has clicked on Cancel or or the escape key
    result_string = 'button returned:Cancel'

  return Result(result_string)
