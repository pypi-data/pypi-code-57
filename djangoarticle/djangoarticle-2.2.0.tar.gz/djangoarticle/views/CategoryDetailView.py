from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme


class CategoryDetailView(ListView):
    template_name = 'djangoadmin/djangoarticle/category_detail_view.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'article_filter'

    def get_queryset(self):
        page = self.request.GET.get("page")
        self.category_detail = get_object_or_404(CategoryModelScheme, slug=self.kwargs['category_slug'])
        article_filter = ArticleModelScheme.objects.filter(category=self.category_detail).filter(is_promote=False)
        article_filter = Paginator(article_filter, 4)
        return article_filter.get_page(page)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context["category_detail"] = self.category_detail
        context['is_promoted'] = ArticleModelScheme.objects.promoted().filter(category=self.category_detail)
        context['is_trending'] = ArticleModelScheme.objects.trending().filter(category=self.category_detail)
        context['promo'] = ArticleModelScheme.objects.promotional().filter(category=self.category_detail)
        return context