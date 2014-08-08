from django.db import models

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('he', 'Hebrew'),
)


URL_MAX_LEN = 300
NAME_MAX_LEN = 130

#TODO: needs to add unique_together to the models

class LanguageField(models.CharField):
    """
    A field for language, defined by the language list above.
    """
    def __init__(self):
        super(LanguageField, self).__init__(max_length=2, choices=LANGUAGES)

class Category(models.Model):
    """
    Model for one Wikipedia category, in one language.
    """
    # The url of the category in Wikipedia
    url = models.CharField(max_length=URL_MAX_LEN)

    # Category name
    name = models.CharField(max_length=NAME_MAX_LEN)

    # Language of the category
    language = LanguageField()

    def get_folder(self):
        """ returns the folder where this category is found in the fs """
        pass

    def get_translated_articles(self):
        # return self.article_set.filter(language__ne=) TODO continue
        pass

    def __unicode__(self):
        return "%s: %s" % (self.language, self.name)


class Article(models.Model):
    """
    Model for a Wikipedia article, which was written in one original language and can have translations.
    """
    # The category of this article
    category = models.ForeignKey(Category)
    # Url from where the article was taken
    url = models.CharField(max_length=URL_MAX_LEN)
    # Article title
    title = models.CharField(max_length=NAME_MAX_LEN)
    # The original language in which the article was written (to be distinguished from the translations)
    original_language = LanguageField()

    # Flag that indicates whether this article is a stub
    is_stub = models.BooleanField()

    def get_original_content(self):
        """
        Return the content written in the original language (and not the translations)
        """
        return self.articlecontent_set.get(language=self.original_language)

    def get_translations(self):
        """
        Return a set of all translations to this article
        """
        return self.articlecontent_set.exclude(language=self.original_language)

    def has_translations(self):
        """
        Returns whether the article has a content which is not in its original language
        """
        return self.get_translations().count() > 0


    def __unicode__(self):
        return "%s: %s, in category %s" % (self.original_language, self.title, self.category.name)


class ArticleContent(models.Model):
    """
    An article content, contains the content of an article in a specific language.
    May be in the original language or a translated content.
    One article may have many contents (in one original language and many translations).
    """
    # The article which this is its content
    article = models.ForeignKey(Article, related_name='articlecontent_set')

    # The language of the text
    language = LanguageField()

    # The article actual content.
    text = models.TextField()

    def is_translated(self):
        return self.article.original_language == self.language

    def __unicode__(self):
        return "%r: content for %r" % (self.language, self.article.title)

