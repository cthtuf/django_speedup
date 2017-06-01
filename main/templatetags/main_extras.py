from django import template

register = template.Library()


def published_articles(regrouped_list, status):
    for group in regrouped_list:
        if group.grouper == status:
            return group.list
    return []

register.filter('published_articles', published_articles)