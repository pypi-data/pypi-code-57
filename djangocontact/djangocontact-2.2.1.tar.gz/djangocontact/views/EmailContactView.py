from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import send_mail
from djangocontact.forms import EmailForm


def EmailContactView(request):
    template_name = "djangoadmin/djangocontact/email_contact_view.html"

    if request.method == "POST":
        # contact forms prefrences here.
        subject = settings.DEFAULT_EMAIL_SUBJECT
        sys_email = settings.DEFAULT_FROM_EMAIL
        email = [request.POST.get('email')]
        full_name = request.POST.get('full_name')
        message = settings.DEFAULT_EMAIL_CONTENT

        # valid and save the email form.
        emailform = EmailForm(request.POST or None)
        if emailform.is_valid():
            emailform.save()

            # context for email.
            context = {"email": email, "sys_email": sys_email, "full_name": full_name, "message": message}
            # get_template for mail.
            mail_template = get_template("djangoadmin/djangocontact/simple_email_template.html").render(context)
            # send mail here.
            send_mail(subject, mail_template, sys_email, email, fail_silently=True)

            # send message here.
            messages.success(request, 'Contact form submitted successfully.', extra_tags='success')
            return redirect('djangocontact:email_contact_view')
        else:
             messages.error(request, 'Contact form not submitted.', extra_tags='warning')
             return redirect('djangocontact:email_contact_view')
    else:
        emailform = EmailForm()
        context = {'emailform': emailform}
        return render(request, template_name, context)