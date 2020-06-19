from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from djangoarticle.models import CategoryModelScheme


class CategoryListDashboard(LoginRequiredMixin, ListView):
    template_name = 'djangoadmin/djangoarticle/category_list_dashboard.html'
    context_object_name = 'category_list'
    paginate_by = 10

    def get_queryset(self):
        category_list = CategoryModelScheme.objects.published()
        query = self.request.GET.get("query")
        if query:
            category_match = CategoryModelScheme.objects.published().filter(Q(title__icontains=query))
            if category_match:
                return category_match
            else:
                return category_list
        else:
            return category_list
        return category_list