from django.shortcuts import render, redirect
from djangopost.models import ArticleModel
from djangocomment.models import CommentModel
from djangocomment.forms import CommentForm


def ArticleDetailView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_detail_view.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    comments = CommentModel.objects.filter_comments_by_instance(article_detail)
    parent_id = None
    if request.method == "POST":
        commentform = CommentForm(request.POST or None)
        try:
            get_parent_id = request.POST["parent_id"]
        except:
            parent_id = None
        else:
            get_parent = CommentModel.objects.get(id=get_parent_id)
            parent_id = int(get_parent.id)
        if commentform.is_valid():
            instance = commentform.save(commit=False)
            instance.author = request.user
            instance.content_type = article_detail.get_for_model
            instance.object_id = article_detail.id 
            instance.parent_id = parent_id
            instance.save()
        return redirect("djangopost:article_detail_view", article_slug = article_slug)
    else:
        commentform = CommentForm()
        context = {'article_detail': article_detail, 'comments': comments, 'commentform': commentform}
        return render(request, template_name, context)