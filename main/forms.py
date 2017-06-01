from django import forms

from .models import (Article, Author)


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('id', 'author', 'description',
                  'text', 'is_published', 'in_archive', )
        widgets = {'id': forms.HiddenInput()}


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('is_active', 'name')
