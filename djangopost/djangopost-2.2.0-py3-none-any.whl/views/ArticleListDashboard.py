from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from djangopost.models import ArticleModel


@login_required()
def ArticleListDashboard(request):
    template_name = 'djangoadmin/djangopost/article_list_dashboard.html'
    article_filter = ArticleModel.objects.author(request.user)
    query = request.GET.get("query")
    if query:
        match = ArticleModel.objects.author(request.user).filter(Q(title__icontains=query))
        if match:
            message = f"Search Results for: {query}."
            messages.add_message(request, messages.SUCCESS, message)
            context = {"article_filter": match}
            return render(request, template_name, context)
        else:
            message = "Nothing matched! Please try again with some different keywords."
            messages.add_message(request, messages.WARNING, message)
            return redirect("djangopost:article_list_dashboard")
    context = {'article_filter': article_filter}
    return render(request, template_name, context)