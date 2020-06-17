from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone

from wafer.schedule.models import ScheduleBlock, Slot, Venue

import yaml


def parse_time(s):
    h, m = s.split(':')
    return time(int(h), int(m))


class Command(BaseCommand):
    help = 'Load Schedule days, venues, and slots from YAML files into the DB'

    def add_arguments(self, parser):
        parser.add_argument('YAMLFILE', help='Input file'),

    def handle(self, *args, **options):
        tz = get_current_timezone()

        with open(options['YAMLFILE']) as f:
            data = yaml.safe_load(f)

        schedule_blocks = {}
        start_of_day = time(0, 0, 0)
        end_of_day = time(23, 59, 59)
        for day in data['days']:
            schedule_block, _ = ScheduleBlock.objects.get_or_create(
                start_time=datetime.combine(day, start_of_day, tz),
                end_time=datetime.combine(day, end_of_day, tz))
            schedule_blocks[day] = schedule_block
            print('Loaded schedule block: %s' % schedule_block)

        for v in data['venues']:
            venue_name = v['name']
            venue, _ = Venue.objects.get_or_create(name=venue_name)
            venue.notes = v['notes']
            venue.order = v['order']
            venue_blocks = [day for d, day in schedule_blocks.items()
                            if d in v['days']]
            venue.blocks.set(venue_blocks)
            venue.save()
            print('Loaded venue: %s (%r)' % (venue, venue_blocks))

        for day, slots in data['slots'].items():
            schedule_block = schedule_blocks[day]
            sb_date = schedule_block.start_time.date()
            for slotdata in slots:
                slot, _ = Slot.objects.get_or_create(
                    name='{}: {}'.format(slotdata['name'], sb_date))
                start_time = parse_time(slotdata['start'])
                slot.start_time = datetime.combine(sb_date, start_time, tz)
                end_time = parse_time(slotdata['end'])
                slot.end_time = datetime.combine(sb_date, end_time, tz)
                slot.save()
                print('Loaded slot: %s' % slot)
