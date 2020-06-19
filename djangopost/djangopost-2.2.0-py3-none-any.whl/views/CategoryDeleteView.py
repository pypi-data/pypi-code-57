from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.models import CategoryModel
from djangotools.decorators import OnlyAuthorAccess


@OnlyAuthorAccess(CategoryModel)
@login_required()
def CategoryDeleteView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_delete_view_form.html'
    category_detail = CategoryModel.objects.get(slug=category_slug)
    if request.method == 'POST':
        category_detail.delete()
        message = f"{category_detail.title} category deleted successfully."
        messages.success(request, message)
        return redirect('djangopost:category_list_dashboard')
    else:
        context = {'category_detail': category_detail }
        return render(request, template_name, context)