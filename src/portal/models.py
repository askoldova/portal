from django.db import models

# Create your models here.
import generation
from . import gen_events


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

        generation.apply_generation_task(gen_events.DefaultPageGenerate(self.lower_code))
        generation.apply_generation_task(gen_events.IndexPageGenerate(), )

    objects = LangManager()

    def __unicode__(self):
        return "%s %s" % (self.code, self.caption)

    str = property(__unicode__)

    lower_code = property(lambda self: self.code.lower())

    class Meta:
        ordering = ("-default", "caption",)


# def class Lang


class LangLocaleManager(models.Manager):
    def get_lang_locale(self, lang, locale):
        if not isinstance(lang, Lang):
            ValueError("%s lang is not a Lang :(" % lang)
        if not isinstance(locale, Lang):
            ValueError("%s locale is not a Lang :(" % lang)

        return self.get(lang=lang, locale=locale)

        # def lang_locale

    def get_queryset(self):
        return super(LangLocaleManager, self).get_queryset().prefetch_related("locale")


# def class LangLocaleManager


class LangLocale(models.Model):
    lang = models.ForeignKey(to=Lang)
    locale = models.ForeignKey(to=Lang, related_name="lang_translated")
    caption = models.CharField(max_length=50)

    objects = LangLocaleManager()

    def __unicode__(self):
        return u"%s>%s %s" % (self.lang.code, self.locale.code, self.caption)

    class Meta:
        unique_together = (("lang", "locale"),)


# def class LangLocale


class MainMenu(models.Model):
    caption = models.CharField(max_length=100, unique=True)
    order = models.SmallIntegerField(default=0)
    hidden = models.BooleanField(default=False)
    width = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ("hidden", "order", "caption")

    def __unicode__(self):
        return u'%s' % (self.caption,)


# def MainMenu


class MainMenuI18nManager(models.Manager):
    def get_queryset(self):
        return super(MainMenuI18nManager, self).get_queryset().prefetch_related("locale")


class MainMenuI18n(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    caption = models.CharField(max_length=100)
    locale = models.ForeignKey(to=Lang)

    objects = MainMenuI18nManager()

    class Meta:
        unique_together = (('menu', 'locale'), ('menu', 'caption'),)
        ordering = ('menu__order', 'locale__code',)

    def __unicode__(self):
        return u'%s>(%s) %s' % (self.menu.caption, self.locale.code, self.caption)


# def MainMenuI18n


class MenuItemManager(models.Manager):
    def get_queryset(self):
        return super(MenuItemManager, self).get_queryset().prefetch_related("menu")


class MenuItem(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    caption = models.CharField(max_length=100)
    order = models.SmallIntegerField(default=0)

    objects = MenuItemManager()

    class Meta:
        unique_together = ('menu', 'caption')
        ordering = ('menu__hidden', 'menu__order', 'order', 'caption')

    def __unicode__(self):
        return u'%s-%s' % (self.menu.caption, self.caption)

# def MenuItem


class MenuItemI18nManager(models.Manager):
    def get_queryset(self):
        return super(MenuItemI18nManager, self).get_queryset().\
            prefetch_related("menu_item", "menu_item__menu", "locale")


class MenuItemI18n(models.Model):
    menu = models.ForeignKey(to=MainMenu)
    menu_item = models.ForeignKey(to=MenuItem)
    caption = models.CharField(max_length=100)
    locale = models.ForeignKey(to=Lang)

    objects = MenuItemI18nManager()

    class Meta:
        unique_together = (('menu_item', 'locale'), ('menu', 'caption', 'locale'))
        ordering = ('menu__order', 'locale__code')

    def __unicode__(self):
        return u'%s-%s>(%s) %s' % (self.menu.caption, self.menu_item.caption,
                                   self.locale.code, self.caption)

# def MenuItemI18n
