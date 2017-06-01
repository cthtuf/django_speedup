from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView, View)
from django.http.response import Http404, JsonResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from .mixin import (NeverCacheMixin, CacheMixin)
from .models import (Article, Author)
from .forms import (ArticleForm, AuthorForm)


# Caching disabled
# Get only needed fields to improve performance
class ArticlesListView(NeverCacheMixin, ListView):
    model = Article
    queryset = Article.objects.filter(in_archive=False)


class ArticleCreateView(NeverCacheMixin, CreateView):
    form_class = ArticleForm
    template_name = 'main/article_create.html'
    success_url = reverse_lazy('articles-list')


class ArticleUpdateView(NeverCacheMixin, UpdateView):
    form_class = ArticleForm
    success_url = reverse_lazy('articles-list')
    kwargs = None

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        super(ArticleUpdateView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        # Load info about author (add join to query)
        return Article.objects.select_related('author').all()

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['object_id'] = self.kwargs['pk']
        return context


class ArticlePublishView(NeverCacheMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(pk=kwargs['pk'])
            article.is_published = True
            # updating just one field to improve performance
            article.save(update_fields=['is_published'])
        except Exception as e:
            messages.error(request, 'There are some error.')
            # pass e.message to client is bad, but it just for example
            return JsonResponse({'success': False, 'error': e.message})
        else:
            messages.success(request, 'The article published successfully.')
            return JsonResponse({
                'success': True,
                'article': article.description
            })


# Don't cache view, but using cache queryset by cacheops
class AuthorDetailView(UpdateView):
    form_class = AuthorForm
    fields = ['is_active', 'name']
