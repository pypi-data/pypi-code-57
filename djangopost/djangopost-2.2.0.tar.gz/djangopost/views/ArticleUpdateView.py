from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.models import ArticleModel
from djangopost.forms import ArticleForm
from djangotools.decorators import OnlyAuthorAccess


@OnlyAuthorAccess(ArticleModel)
@login_required()
def ArticleUpdateView(request, article_slug):
    template_name = 'djangoadmin/djangopost/article_create_view_form.html'
    article_detail = ArticleModel.objects.get(slug=article_slug)
    if request.method == 'POST':
        articleform  = ArticleForm(request.POST or None, request.FILES or None, instance=article_detail)
        if articleform.is_valid():
            instance = articleform.save(commit=False)
            instance.author = request.user
            instance.save()
            message = f"{articleform.cleaned_data['title']} article updated successfully."
            messages.success(request, message)
            return redirect('djangopost:article_list_dashboard')
        else:
            message = f"{request.POST['title']} article not updated! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:article_list_dashboard')
    else:
        articleform = ArticleForm(instance=article_detail)
        context = { 'article_form': articleform }
        return render(request, template_name, context)