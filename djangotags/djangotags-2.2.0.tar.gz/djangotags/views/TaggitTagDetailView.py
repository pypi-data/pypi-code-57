from django.views.generic import DetailView
from taggit.models import Tag
from djangoarticle.models import ArticleModelScheme


class TaggitTagDetailView(DetailView):
    template_name = "djangoadmin/djangotags/taggit_tag_detail_view.html"
    model = Tag
    slug_url_kwarg = "tag_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lookup_instance = self.kwargs['tag_slug']
        context['article_filter'] = ArticleModelScheme.objects.published().filter(tags__slug=lookup_instance, is_promote=False)
        context['is_promoted'] = ArticleModelScheme.objects.promoted().filter(tags__slug=lookup_instance)
        context['promo'] = ArticleModelScheme.objects.promotional()
        context['is_trending'] = ArticleModelScheme.objects.trending()
        return context