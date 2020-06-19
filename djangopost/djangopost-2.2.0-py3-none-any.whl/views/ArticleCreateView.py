from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.forms import ArticleForm


@login_required()
def ArticleCreateView(request):
    template_name = 'djangoadmin/djangopost/article_create_view_form.html'
    if request.method == 'POST':
        articleform = ArticleForm(request.POST or None, request.FILES or None)
        if articleform.is_valid():
            instance = articleform.save(commit=False)
            instance.author = request.user
            instance.save()
            message = f"{articleform.cleaned_data['title']} article created successfully."
            messages.success(request, message)
            return redirect('djangopost:article_list_dashboard')
        else:
            message = f"{request.POST['title']} article not created! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:article_create_view')
    else:
        articleform = ArticleForm()
        context = {'article_form': articleform}
        return render(request, template_name, context)