from django.views.generic import ListView
from djangoarticle.models import ArticleModelScheme


class ArticleListView(ListView):
    template_name = 'djangoadmin/djangoarticle/article_list_view.html'
    context_object_name = 'article_filter'

    def get_queryset(self):
        return ArticleModelScheme.objects.published().filter(is_promote=False)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['is_promoted'] = ArticleModelScheme.objects.promoted()
        context['is_trending'] = ArticleModelScheme.objects.trending()
        context['promo'] = ArticleModelScheme.objects.promotional()
        context['opinions'] = ArticleModelScheme.objects.opinion()[0:2]
        return context