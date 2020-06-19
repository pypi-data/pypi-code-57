from djangopost.models import CategoryModel


def CategoryContext(request):
    djangopost_category = CategoryModel.objects.published()
    return {"djangopost_category": djangopost_category}