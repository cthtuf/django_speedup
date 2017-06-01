from datetime import datetime

from django.db import models


class Author(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    __original_is_published = None

    is_published = models.BooleanField(default=False)
    in_archive = models.BooleanField(default=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_modified = models.DateTimeField(auto_now=True)
    dt_published = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('main.author')
    description = models.CharField(max_length=255)
    text = models.TextField()

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.__original_is_published = self.is_published

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        # set date
        self.dt_modified = datetime.now()
        if not self.__original_is_published and self.is_published:
            self.dt_published = datetime.now()
        elif self.__original_is_published and not self.is_published:
            self.dt_published = None

        super(Article, self).save(*args, **kwargs)
        self.__original_is_published = self.is_published
