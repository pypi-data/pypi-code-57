import yaml
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand


from volunteers.models import TaskCategory, TaskTemplate, Task
from wafer.schedule.models import Venue


class Command(BaseCommand):
    help = 'Creates volunteer tasks from a YAML file'

    def add_arguments(self, parser):
        parser.add_argument('FILE', type=open)

    def handle(self, *args, **options):
        data = yaml.safe_load(options['FILE'])

        tasks = 0
        for item in data['tasks']:
            category, _ = TaskCategory.objects.get_or_create(name=item['category'])

            template, _ = TaskTemplate.objects.get_or_create(
                name=item['name']
            )
            if 'nbr_volunteers_min' in item:
                template.nbr_volunteers_min = item['nbr_volunteers_min']
            if 'nbr_volunteers_max' in item:
                template.nbr_volunteers_min = item['nbr_volunteers_max']
            if 'description' in item:
                template.description = item['description']
            if 'nbr_volunteers_max' in item or 'nbr_volunteers_max' in item or 'description' in item:
                template.save()

            if 'venues' in item:
                venues = []
                for v in item['venues']:
                    venue, _ = Venue.objects.get_or_create(name=v)
                    venues.append(venue)
            else:
                venues = [None]

            for day in item['days']:
                for hour in item['hours']:
                    startstr = hour['start']
                    endstr = hour['end']
                    start = timezone.make_aware(
                        datetime.strptime('%s %s' % (day, startstr), '%Y-%m-%d %H:%M')
                    )
                    end = timezone.make_aware(
                        datetime.strptime('%s %s' % (day, endstr), '%Y-%m-%d %H:%M')
                    )

                    for venue in venues:
                        task, _ = Task.objects.get_or_create(
                            template=template,
                            start=start,
                            end=end,
                            venue=venue,
                        )
                        print('Created task: %s' % task)
                        tasks = tasks + 1
        print('Tasks created: %d' % tasks)
