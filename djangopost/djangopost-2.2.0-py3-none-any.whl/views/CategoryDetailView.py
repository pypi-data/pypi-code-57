from django.shortcuts import render
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel


def CategoryDetailView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_detail_view.html'
    category_detail = CategoryModel.objects.get(slug=category_slug)
    article_filter = ArticleModel.objects.published().filter(category=category_detail).filter(is_promote=False)
    is_promoted = ArticleModel.objects.promoted().filter(category=category_detail)
    is_trending = ArticleModel.objects.trending().filter(category=category_detail)
    promo = ArticleModel.objects.promotional().filter(category=category_detail)
    context = {'category_detail': category_detail, 'article_filter': article_filter, 'is_promoted': is_promoted, 'is_trending': is_trending, "promo": promo}
    return render(request, template_name, context)