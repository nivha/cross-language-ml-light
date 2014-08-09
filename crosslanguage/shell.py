import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category, Article, ArticleContent

a = Article.objects.get(pk=1)
