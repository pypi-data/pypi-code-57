from django.shortcuts import render
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel


def ArticleListView(request):
    template_name = 'djangoadmin/djangopost/article_list_view.html'
    category_filter = CategoryModel.objects.published()
    article_filter = ArticleModel.objects.published().filter(is_promote=False)
    is_promoted = ArticleModel.objects.promoted()
    is_trending = ArticleModel.objects.trending()
    promo = ArticleModel.objects.promotional()
    opinions = ArticleModel.objects.opinion()
    context = {'category_filter': category_filter, 'article_filter': article_filter,
               'is_promoted': is_promoted, 'is_trending': is_trending, 'promo': promo,
               'opinions': opinions}
    return render(request, template_name, context)