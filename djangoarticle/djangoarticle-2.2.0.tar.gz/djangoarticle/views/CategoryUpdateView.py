from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from djangoarticle.models import CategoryModelScheme
from djangoarticle.forms import CategoryFormScheme
from djangotools.mixins import OnlyAuthorAccess


class CategoryUpdateView(LoginRequiredMixin, OnlyAuthorAccess, SuccessMessageMixin, UpdateView):
    model = CategoryModelScheme
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "Category updated successfully."

    def get_success_message(self, cleaned_data):
        return "{} {}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"Sorry! {form.instance.title} category not updated."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context