import collections
from django.db import models

# Create your models here.
import generation
import portal.objects


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Lang, self).save(force_insert, force_update, using, update_fields)

        generation.schedule_generation.apply_async((DefaultPageGenerate(self.code.lower()),))
        generation.schedule_generation.apply_async((IndexPageGenerate(),))

    objects = LangManager()

    def __unicode__(self):
        return "%s %s" % (self.code, self.caption)

    str = property(__unicode__)

    class Meta:
        ordering=("-default", "caption", )
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
        return u"%s>%s %s" % (self.lang.code, self.locale.code, self.caption)

    class Meta:
        unique_together=(("lang", "locale"), )
# def class LangLocale

class MainMenu(models.Model):
    caption = models.CharField(max_length=100, unique=True)
    locale = models.ForeignKey(to=Lang)
    order = models.SmallIntegerField(default=0)
    hidden = models.BooleanField(default=False)
    width = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ("hidden", "order", "caption")

    def __unicode__(self):
        return u'%s(%s)' % (self.caption, self.locale.code)
# def MainMenu

class MainMenuI18n(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    caption = models.CharField(max_length=100)
    locale = models.ForeignKey(to=Lang)

    class Meta:
        unique_together = (('menu', 'locale'), ('menu', 'caption'),)
        ordering = ('menu__order', 'locale__code',)

    def __unicode__(self):
        return u'%s>(%s) %s' % (self.menu.caption, self.locale.code, self.caption)

# def MainMenuI18n

class MenuItem(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    caption = models.CharField(max_length=100)
    locale = models.ForeignKey(to=Lang)
    order = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('menu', 'caption', 'locale')
        ordering = ('menu__hidden', 'menu__order', 'order', 'caption')

    def __unicode__(self):
        return u'%s-%s(%s)' % (self.menu.caption, self.caption, self.locale.code)
# def MenuItem

class MenuItemI18n(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    menu_item = models.ForeignKey(to=MenuItem)
    caption = models.CharField(max_length=100)
    locale = models.ForeignKey(to=Lang)

    class Meta:
        unique_together = (('menu_item', 'locale'), ('menu', 'caption', 'locale'))
        ordering = ('menu__order', 'locale__code')

    def __unicode__(self):
        return u'%s-%s>(%s) %s' % (self.menu.caption, self.menu_item.caption,
                                   self.locale.code, self.caption)

# def MenuItemI18n
class DefaultPageGenerate:
    def __init__(self, language_code):
        self.language_code = language_code

    def __repr__(self):
        return u"DefaultPageGenerate(%s)" % (dict(language_code=self.language_code),)

    @property
    def language_code(self):
        return self.language_code



class IndexPageGenerate:
    def __init__(self):
        pass

    def __repr__(self):
        return u'IndexPageGenerate'

# class IndexPageGenerate
