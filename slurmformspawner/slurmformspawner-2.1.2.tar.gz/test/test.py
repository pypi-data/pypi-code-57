from slurmformspawner import form

x = form.SlurmSubmitForm('felix')
print(x.render())

from slurmformspawner import SlurmFormSpawner

y = SlurmFormSpawner(username='felix')