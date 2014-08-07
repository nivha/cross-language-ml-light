from django.contrib import admin
from models import Category
from models import Article
from models import ArticleContent
from django.forms.widgets import Textarea
from django.db import models


class ArticleContentInline(admin.TabularInline):
    model = ArticleContent
    extra = 0
    fields = ('language', 'text')
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows': 7, 'cols': 100})}, }


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'original_language')
    inlines = [ArticleContentInline]


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleContent)

# Register your models here.
