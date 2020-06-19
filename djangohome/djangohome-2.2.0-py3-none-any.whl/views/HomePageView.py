from django.views.generic import ListView
from djangoarticle.models import ArticleModelScheme


class HomePageView(ListView):
    template_name = "djangoadmin/djangohome/homepage_view.html"
    context_object_name = "article_filter"

    def get_queryset(self):
        article_filter = ArticleModelScheme.objects.published().filter(is_promote=False)
        return article_filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_promoted'] = ArticleModelScheme.objects.promoted()
        context['is_trending'] = ArticleModelScheme.objects.trending()
        context['promo'] = ArticleModelScheme.objects.promotional()
        context['opinions'] = ArticleModelScheme.objects.opinion()
        return context