from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from djangoadmin.forms import RegistrationForm


def SignupView(request):
    template_name = 'djangoadmin/djangoadmin/signup_view_form.html'
    if request.method == 'POST':
        usercreationform = RegistrationForm(request.POST)
        if usercreationform.is_valid():
            user = usercreationform.save()
            login(request, user)
            messages.success(request, f"Hello!, {user.first_name} Welcome to Djangoengine.", extra_tags='success')
            return redirect('djangoadmin:account_view')
        else:
            messages.error(request, "Ohh!, Something went wrong, Please try again.", extra_tags='warning')
            return redirect('djangoadmin:signup_view')
    else:
        usercreationform = RegistrationForm()
        context = { 'usercreationform': usercreationform }
        return render(request, template_name, context)