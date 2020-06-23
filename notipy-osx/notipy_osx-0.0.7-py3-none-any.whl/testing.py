# This file is never used in the modules. It is only meant for testing parts of the package

try:
  from notipy_osx import dialog_prompt, notify
except:
  from __init__ import dialog_prompt, notify

notify(title='New Notifiation', delay=5)

a = dialog_prompt('First', buttons=['Yes', 'No'])
print(a.button_returned)