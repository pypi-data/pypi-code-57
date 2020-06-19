from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from djangoarticle.forms import CategoryFormScheme


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    success_message = "Category created successfully."

    def get_success_message(self, cleaned_data):
        return "{0} {1}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryCreateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"{form.instance.title} category not created! Please try some different keywords."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context