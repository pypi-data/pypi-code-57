from djangoarticle.models import CategoryModelScheme


def CategoryContext(request):
    article_category = CategoryModelScheme.objects.published()
    return {"article_category": article_category}