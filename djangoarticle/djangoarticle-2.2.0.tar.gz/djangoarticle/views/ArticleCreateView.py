from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from djangoarticle.models import ArticleModelScheme
from djangoarticle.forms import CategoryFormScheme, ArticleFormScheme


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ArticleFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    success_message = "article created successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context