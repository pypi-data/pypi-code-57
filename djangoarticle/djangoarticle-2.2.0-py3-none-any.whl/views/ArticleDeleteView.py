from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from djangoarticle.models import ArticleModelScheme
from djangotools.mixins import OnlyAuthorAccess


class ArticleDeleteView(LoginRequiredMixin, OnlyAuthorAccess, DeleteView):
    model = ArticleModelScheme
    context_object_name = 'article_detail'
    template_name = 'djangoadmin/djangoarticle/article_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['article_slug']} {self.success_message}."
        messages.warning(self.request, message)
        return super(ArticleDeleteView, self).delete(request, *args, **kwargs)