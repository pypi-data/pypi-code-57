from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.models import CategoryModel
from djangopost.forms import CategoryForm
from djangotools.decorators import OnlyAuthorAccess


@OnlyAuthorAccess(CategoryModel)
@login_required()
def CategoryUpdateView(request, category_slug):
    template_name = 'djangoadmin/djangopost/category_create_view_form.html'
    category_detail = CategoryModel.objects.get(slug=category_slug)
    if request.method == 'POST':
        categoryform  = CategoryForm(request.POST or None, instance=category_detail)
        if categoryform.is_valid():
            categoryform.save()
            message = f"{categoryform.cleaned_data.get('title')} category updated successfully."
            messages.success(request, message)
            return redirect('djangopost:category_list_dashboard')
        else:
            message = f"Sorry! {request.POST['title']} category not updated."
            messages.warning(request, message)
            return redirect('djangopost:category_list_dashboard')
    else:
        categoryform = CategoryForm(instance=category_detail)
        context = { 'category_form': categoryform }
        return render(request, template_name, context)