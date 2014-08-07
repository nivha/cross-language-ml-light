import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category, Article, ArticleContent

a = Article.objects.get(pk=1)

from clml.BoxA import *
trainc = Category.objects.filter(language='en')
testc = Category.objects.filter(language='es')
s = SimpleClassifierTester('en', 'es', trainc, testc, Direction.Pre)
s._train()
