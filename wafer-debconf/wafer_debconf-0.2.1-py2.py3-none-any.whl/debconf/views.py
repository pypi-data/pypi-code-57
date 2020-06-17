from collections import defaultdict

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.views.generic import TemplateView, View

from wafer.talks.models import Talk, Track
from wafer.schedule.views import ScheduleView
from wafer.schedule.models import Venue, ScheduleItem, Slot

from register.models import Attendee
from front_desk.models import CheckIn


class DCScheduleArrived(View):
    def arrived_users(self):
        queryset = Attendee.objects.filter(announce_me=True).select_related(
            'user',
            'user__userprofile',
            'check_in',
        )
        now = timezone.now()
        for attendee in queryset:
            user = attendee.user
            try:
                arrived = attendee.check_in is not None
            except CheckIn.DoesNotExist:
                arrived = False

            departed = False
            if attendee.departure:
                departed = attendee.departure < now

            yield {
                'username': user.username,
                'arrived': arrived,
                'departed': departed,
                'name': user.userprofile.display_name(),
                'nick': attendee.nametag_3,
            }

    def get(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        auth = auth_header.split(None, 1)
        if not constant_time_compare(auth, ['Bearer', settings.DCSCHEDULE_TOKEN]):
            raise PermissionDenied('Missing/Invalid Authorization token')
        return JsonResponse({
            'arrived': list(self.arrived_users())
        })


class RobotsView(TemplateView):
    template_name = 'debconf/robots.txt'
    content_type = 'text/plain; charset=UTF-8'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SANDBOX'] = settings.SANDBOX
        return context


class DebConfScheduleView(ScheduleView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = Track.objects.all()
        return context


def get_current_slot():
    now = timezone.now()

    for slot in Slot.objects.all():
        start = slot.start_time
        end = slot.end_time
        if start <= now and now < end:
            return slot


class IndexView(TemplateView):
    template_name = 'wafer/index.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        venues = Venue.objects.filter(video=True)

        venue_blocks = [{'venue': venue} for venue in venues]

        current_slot = get_current_slot()
        if current_slot:
            events = ScheduleItem.objects.filter(slots=current_slot)
            for event in events:
                for blk in venue_blocks:
                    if event.venue == blk['venue']:
                        slots = list(event.slots.all())
                        blk['event'] = event
                        blk['start_time'] = slots[0].get_formatted_start_time()
                        blk['end_time'] = slots[-1].get_formatted_end_time()

        context_data['venue_blocks'] = venue_blocks

        return context_data


class StatisticsView(TemplateView):
    template_name = 'debconf/statistics.html'


class ContentStatisticsView(TemplateView):
    template_name = 'debconf/content_statistics.html'
    cache_key = 'debconf:content_statistics'
    cache_timeout = 30*60 if not settings.DEBUG else 10

    def get_context_data(self, **kwargs):
        retval = cache.get(self.cache_key)
        if retval:
            return retval

        talks_submitted = Talk.objects.count()
        talks_reviewed = Talk.objects.filter(
            reviews__isnull=False).distinct().count()
        talks_scheduled = Talk.objects.filter(
            scheduleitem__isnull=False).distinct().count()

        minutes_of_content = 0
        for si in ScheduleItem.objects.filter(talk__isnull=False):
            duration = si.get_duration()
            minutes_of_content += duration['minutes'] + duration['hours'] * 60
        hours_of_content = minutes_of_content / 60

        concurrency_by_hour = defaultdict(int)
        for slot in Slot.objects.all():
            hour = slot.start_time.replace(
                minute=0, second=0, microsecond=0)
            concurrency_by_hour[hour] = max(concurrency_by_hour[hour],
                                            slot.scheduleitem_set.count())

        hours_of_concurrency = []
        if concurrency_by_hour:
            hours_of_concurrency = [
                (concurrency, sum(
                    1 for hour, hour_concurrency in concurrency_by_hour.items()
                    if hour_concurrency == concurrency))
                for concurrency in range(max(concurrency_by_hour.values()) + 1)]

        talks_by_track = {}
        for track in Track.objects.all():
            talks_by_track[track.name] = {
                'submitted': track.talk_set.count(),
                'scheduled': track.talk_set.filter(
                    scheduleitem__isnull=False).count(),
            }

        retval = {
            'talks_submitted': talks_submitted,
            'talks_reviewed': talks_reviewed,
            'talks_scheduled': talks_scheduled,
            'hours_of_content': hours_of_content,
            'hours_of_concurrency': hours_of_concurrency,
            'talks_by_track': talks_by_track,
        }

        cache.set(self.cache_key, retval, self.cache_timeout)
        return retval
