from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from djangopost.forms import CategoryForm


@login_required()
def CategoryCreateView(request):
    template_name = 'djangoadmin/djangopost/category_create_view_form.html'
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST or None)
        if categoryform.is_valid():
            instance = categoryform.save(commit=False)
            instance.author = request.user
            instance.save()
            # Without this next line the tags won't be saved.
            categoryform.save_m2m()
            message = f"{categoryform.cleaned_data['title']} category created successfully."
            messages.success(request, message)
            return redirect('djangopost:category_list_dashboard')
        else:
            message = f"{request.POST['title']} category not created! Please try some different keywords."
            messages.warning(request, message)
            return redirect('djangopost:category_create_view')
    else:
        categoryform = CategoryForm()
        context = { 'category_form': categoryform }
        return render(request, template_name, context)