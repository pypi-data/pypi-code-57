from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.contrib.contenttypes.models import ContentType
from djangoarticle.models import ArticleModelScheme
from djangocomment.models import CommentModel
from djangocomment.forms import CommentForm


class ArticleDetailGetView(DetailView):
    model = ArticleModelScheme
    template_name = 'djangoadmin/djangoarticle/article_detail_view.html'
    context_object_name = 'article_detail'
    slug_url_kwarg = 'article_slug'

    def get_object(self, **kwargs):
        object = super(ArticleDetailGetView, self).get_object(**kwargs)
        object.total_views += 1
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailGetView, self).get_context_data(**kwargs)
        article_detail = ArticleModelScheme.objects.get(slug=self.kwargs['article_slug'])
        context["comments"] = CommentModel.objects.filter_comments_by_instance(article_detail)
        context['commentform'] = CommentForm()
        return context


class ArticleDetailFormView(FormView):
    template_name = 'djangoadmin/djangoarticle/article_detail_view.html'
    form_class = CommentForm
    parent_id = None

    def form_valid(self, form):
        article_detail = ArticleModelScheme.objects.get(slug=self.kwargs['article_slug'])
        try:
            get_parent_id = self.request.POST["parent_id"]
        except:
            parent_id = self.parent_id
        else:
            get_parent = CommentModel.objects.get(id=get_parent_id)
            parent_id = int(get_parent.id)
        form.instance.author = self.request.user
        form.instance.content_type = article_detail.get_for_model
        form.instance.object_id = article_detail.id 
        form.instance.parent_id = parent_id
        form.save()
        return redirect("djangoarticle:article_detail_view", article_slug=self.kwargs['article_slug'])


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDetailGetView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleDetailFormView.as_view()
        return view(request, *args, **kwargs)