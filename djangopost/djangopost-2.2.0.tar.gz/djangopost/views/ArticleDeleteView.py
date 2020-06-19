from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.models import ArticleModel
from djangotools.decorators import OnlyAuthorAccess


@OnlyAuthorAccess(ArticleModel)
@login_required()
def ArticleDeleteView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_delete_view_form.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    if request.method == 'POST':
        article_detail.delete()
        message = f"{article_detail.title} article deleted successfully."
        messages.success(request, message)
        return redirect('djangopost:article_list_dashboard')
    else:
        context = {'article_detail': article_detail }
        return render(request, template_name, context)