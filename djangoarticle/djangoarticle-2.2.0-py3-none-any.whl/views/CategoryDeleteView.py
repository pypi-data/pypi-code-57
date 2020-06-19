from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from djangoarticle.models import CategoryModelScheme
from djangotools.mixins import OnlyAuthorAccess


class CategoryDeleteView(LoginRequiredMixin, OnlyAuthorAccess, DeleteView):
    model = CategoryModelScheme
    context_object_name = 'category_detail'
    template_name = 'djangoadmin/djangoarticle/category_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "category deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['category_slug']} {self.success_message}"
        messages.add_message(self.request, messages.WARNING, message)
        return super(CategoryDeleteView, self).delete(request, *args, **kwargs)