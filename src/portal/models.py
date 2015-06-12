from django.db import models

# Create your models here.

class LangManager(models.Manager):
    def get_default(self):
        return self.get(default=True)

    # def get_default

    def get_by_code(self, code):
        return self.get(code=code)
    # def get_by_code
# def LangManager


class Lang(models.Model):
    code = models.CharField(max_length=2)
    caption = models.CharField(max_length=50)
    default = models.BooleanField(default=False)

    objects = LangManager()

    def __unicode__(self):
        return "%s %s" % (self.code, self.caption)

    str = property(__unicode__)

# def class Lang

class LangLocaleManager(models.Manager):
    def get_lang_locale(self, lang, locale):
        if not isinstance(lang, Lang):
            ValueError("%s lang is not a Lang :(" % lang)
        if not isinstance(locale, Lang):
            ValueError("%s locale is not a Lang :(" % lang)

        return self.get(lang=lang, locale=locale)

    # def lang_locale

# def class LangLocaleManager

class LangLocale(models.Model):
    lang = models.ForeignKey(to=Lang)
    locale = models.ForeignKey(to=Lang, related_name="lang_translated")
    caption = models.CharField(max_length=50)

    objects = LangLocaleManager()

    def __unicode__(self):
        return "%s>%s %s" % (self.lang.code, self.locale.code, self.caption)

# def class LangLocale
