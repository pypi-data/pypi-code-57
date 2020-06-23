# pylint: disable=import-error
from notification import notify
from dialog import dialog_prompt

# notify(title='New Notifiation', delay=3)

a = dialog_prompt('First', buttons=['Yes', 'No'])
print(a.button_returned)