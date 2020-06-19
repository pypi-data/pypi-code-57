from taggit.models import Tag


def TaggitTagListContext(request):
    taglist = Tag.objects.all().order_by('-pk')[0:10]
    return {'taglist': taglist}