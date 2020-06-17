from django.conf.urls import url

from debconf.views import (
    ContentStatisticsView, DCScheduleArrived, DebConfScheduleView, IndexView,
    RobotsView, StatisticsView,
)

urlpatterns = [
    url(r'^attendees/admin/export/arrived/$', DCScheduleArrived.as_view()),
    url(r'^schedule/$', DebConfScheduleView.as_view(),
        name='wafer_full_schedule'),
    url(r'^robots.txt$', RobotsView.as_view()),
    url(r'^$', IndexView.as_view()),
    url(r'^statistics/$', StatisticsView.as_view()),
    url(r'^talks/statistics/$', ContentStatisticsView.as_view(),
        name='content-statistics'),
]
