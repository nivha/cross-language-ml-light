# coding=utf-8

import os
import ujson

from fetcher.utils import cat_lang


os.environ["DJANGO_SETTINGS_MODULE"] = 'crosslanguage.settings'
from django.conf import settings

from clml.models import Category, Article, ArticleContent


def load_category(language, category_name):
    """
    Load a category to the DB.
    Includes creating the category, loading the articles and all their translations.
    """

    # Resolve the category URL
    category_url = u'http://{:s}.wikipedia.org/wiki/{:s}:{:s}'.format(
        language, cat_lang[language], category_name)

    # Get path in
    path = os.path.join(settings.DATA_DIR, language, category_name)
    print 'Loading category from path:', path

    # Create django category in database
    category, _ = Category.objects.get_or_create(
        url=category_url,
        name=category_name,
        language=language,
    )

    # Load all article in path directory.
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)): continue
        # Exclude all non .txt files
        if not filename.endswith('.txt'):
            raise Exception('{:s} is not a txt file - what is it doing here?'.format(filename))

        with open(os.path.join(path, filename)) as f:
            json = f.read()
            d = ujson.loads(json)
            text = d['text']
            title = os.path.splitext(filename)[0]
            article_url = 'http://{:s}.wikipedia.org/wiki/{:s}'.format(
                language, title)

            article, _ = Article.objects.get_or_create(
                category=category,
                url=article_url,
                title=title,
                original_language=language,
                is_stub=False  # TODO - check in some way whether this is a stub
            )

            article_content, _ = ArticleContent.objects.get_or_create(
                article=article,
                language=article.original_language,
                text=text,
            )

    # Load translations:
    for lang_dir in os.listdir(path):
        # Exclude all non directories
        if not os.path.isdir(os.path.join(path, lang_dir)):
            continue

        print 'lang_dir:', lang_dir

        # Load all article in path directory.
        for filename in os.listdir(os.path.join(path, lang_dir)):
            # Exclude all non .txt files
            if not filename.endswith('.txt'):
                continue

            with open(os.path.join(path, lang_dir, filename)) as f:
                # json = f.read()
                # d = ujson.loads(json)
                # text = d['text']
                text = f.read()

                article_url = 'http://'+language+'.wikipedia.org/wiki/' + category_name

                title = os.path.splitext(filename)[0]

                print 'getting article: lang=',language, "category=",category_name, "title=",title

                article = Article.objects.get(original_language=language,
                                              category__name=category_name,
                                              title=title)

                print 'adding ' + lang_dir + ' translation to ' + article.title + ' , originally in ' + language
                article_content = ArticleContent.objects.get_or_create(
                    article=article,
                    language=lang_dir,
                    text=text,
                )


def load_language(language):
    """
    Load all categories of a language, to the DB.
    """
    # lang = Language.path_to_lang[lang_path]
    for category_path in os.listdir(os.path.join(settings.DATA_DIR, language)):
        load_category(language, category_path)


def clean_all():
    """
    Cleans all DB..
    """
    Category.objects.all().delete()


if __name__ == '__main__':
    # clean_all()

    # load_language('en')
    # load_language('es')

    # load_category('en', 'Latin_American_art')
    load_category('en', 'Asian_art')
    load_category('es', 'Arte_latinoamericano')
    load_category('es', 'Arte_de_Asia')
    pass



