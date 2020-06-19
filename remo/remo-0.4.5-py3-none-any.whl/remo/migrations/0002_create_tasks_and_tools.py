from __future__ import unicode_literals

from django.db import migrations

from remo_app.remo.api.constants import ToolType, TaskType, task_tools_mapping


def create_tasks_and_tools(apps, schema_editor):
    task_model = apps.get_model('remo', 'Task')
    tool_model = apps.get_model('remo', 'Tool')

    for _, value in ToolType.choices():
        if tool_model.objects.filter(code_name=value).count() == 0:
            tool_model.objects.create(code_name=value)

    for name, value in TaskType.choices():
        if task_model.objects.filter(name=value, type=name).count() == 0:
            task_model.objects.create(name=value, type=name)

    for task, tool in task_tools_mapping.items():
        db_task = task_model.objects.get(type=task.name)
        db_tool = tool_model.objects.get(code_name=tool.value)

        existing_tools = {t.code_name for t in db_task.available_tools.all()}
        if tool.value in existing_tools:
            continue
        db_task.available_tools.add(db_tool)
        db_task.save()


class Migration(migrations.Migration):
    dependencies = [
        ('remo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_tasks_and_tools),
    ]
