from django.conf.urls import url

from .views import (ArticlesListView, ArticleCreateView, ArticleUpdateView, AuthorDetailView,
                    ArticlePublishView)

urlpatterns = [
    url(r'^articles/$', ArticlesListView.as_view(),
        name='articles-list'),
    url(r'^article/create/$', ArticleCreateView.as_view(),
        name='article-create'),
    url(r'^article/(?P<pk>\d+)/$', ArticleUpdateView.as_view(),
        name='article-update'),
    url(r'^article/(?P<pk>\d+)/publish/$', ArticlePublishView.as_view(),
        name='article-publish'),
    url(r'^author/(?P<pk>\d+)/$', AuthorDetailView.as_view(),
        name='author-detail'),
]