from django.apps import AppConfig


class RemoConfig(AppConfig):
    name = 'remo_app.remo'

    # def ready(self):
    #     from remo_app.remo.use_cases import is_remo_local
    #
    #     if not is_remo_local():
    #         from remo_app.remo.use_cases.jobs.scheduled_jobs import schedule_jobs
    #         schedule_jobs()
