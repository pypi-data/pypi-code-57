from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserDateSearchMixin(object):
    def get_queryset(self):
        queryset = super().get_queryset()

        user_query = self.request.GET.get("user", None)
        date_query = self.request.GET.get("date", None)
        date2_query = self.request.GET.get("date2", None)

        # USER
        if user_query:
            user_lookup = Q()

            user_lookup = user_lookup | Q(**{User.USERNAME_FIELD: user_query})

            for key in User.REQUIRED_FIELDS:
                user_lookup = user_lookup | Q(**{key: user_query})

            user = User.objects.filter(user_lookup)

            if user.exists():
                queryset = queryset.filter(user__in=user)

        # Date & Date2
        if date_query:
            date_lookup = Q()

            try:
                date_lookup = date_lookup | Q(datetime__date__gte=datetime.strptime(date_query, "%Y-%m-%d").date())

                queryset = queryset.filter(date_lookup)

                try:
                    if date2_query:
                        date_lookup = date_lookup & Q(
                            datetime__date__lte=datetime.strptime(date2_query, "%Y-%m-%d").date()
                        )
                except BaseException:
                    pass
            except BaseException:
                pass

            queryset = queryset.filter(date_lookup)
        return queryset


class PaginationMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        # paginate_by = self.get_paginate_by(queryset)
        page_q = self.paginate_queryset(queryset, self.get_paginate_by(queryset))
        begin_pages = 5
        end_pages = 5
        before_pages = 5
        after_pages = 5
        page = page_q[1]
        get_string = ""
        for key, value in self.request.GET.items():
            if key != "page":
                get_string += "&%s=%s" % (key, value)

        page_range = list(page.paginator.page_range)
        begin = page_range[:begin_pages]
        end = page_range[-end_pages:]
        middle = page_range[max(page.number - before_pages - 1, 0) : page.number + after_pages]

        if set(begin) & set(middle):  # [1, 2, 3], [2, 3, 4], [...]
            begin = sorted(set(begin + middle))  # [1, 2, 3, 4]
            middle = []
        elif begin[-1] + 1 == middle[0]:  # [1, 2, 3], [4, 5, 6], [...]
            begin += middle  # [1, 2, 3, 4, 5, 6]
            middle = []
        elif middle[-1] + 1 == end[0]:  # [...], [15, 16, 17], [18, 19, 20]
            end = middle + end  # [15, 16, 17, 18, 19, 20]
            middle = []
        elif set(middle) & set(end):  # [...], [17, 18, 19], [18, 19, 20]
            end = sorted(set(middle + end))  # [17, 18, 19, 20]
            middle = []

        if set(begin) & set(end):  # [1, 2, 3], [...], [2, 3, 4]
            begin = sorted(set(begin + end))  # [1, 2, 3, 4]
            middle, end = [], []
        elif begin[-1] + 1 == end[0]:  # [1, 2, 3], [...], [4, 5, 6]
            begin += end  # [1, 2, 3, 4, 5, 6]
            middle, end = [], []

        context["page_range"], context["begin"], context["end"], context["middle"] = (page_range, begin, end, middle)

        # print(context)

        return context
