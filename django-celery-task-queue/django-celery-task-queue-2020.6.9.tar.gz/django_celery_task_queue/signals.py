from django.db.models.signals import ModelSignal

task_completed = ModelSignal()
task_deleted = ModelSignal()
task_disabled = ModelSignal()
task_restarted = ModelSignal()
