from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.models import CategoryModel


@login_required()
def CategoryListDashboard(request):
    template_name = 'djangoadmin/djangopost/category_list_dashboard.html'
    category_list = CategoryModel.objects.published()
    query = request.GET.get("query")
    if query:
        match = CategoryModel.objects.published().filter(Q(title__icontains=query))
        if match:
            message = f"Search Results for: {query}."
            messages.success(request, message)
            context = {"category_list": match}
            return render(request, template_name, context)
        else:
            message = "Nothing matched! Please try again with some different keywords."
            messages.warning(request, message)
            return redirect("djangopost:category_list_dashboard")
    context = {'category_list': category_list}
    return render(request, template_name, context)