from setuptools import setup

setup(
    name='django-celery-task-queue',
    version='2020.6.9',
    install_requires=[
        'Django',
        'Requests',
        'setuptools',
    ],
    packages=[
        'django_celery_task_queue',
        'django_celery_task_queue.migrations',
        'django_celery_task_queue.models',
    ],
)
