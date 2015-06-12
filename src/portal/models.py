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
        ordering = ('menu__order', 'order', 'caption')

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
