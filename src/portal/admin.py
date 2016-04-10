from django import forms
from django.conf import settings
from django.contrib import admin

from . import models
# noinspection PyUnresolvedReferences
from . import generators
from django.core import urlresolvers


class LangLocaleAdmin(admin.TabularInline):
    model = models.LangLocale
    fk_name = 'lang'
    extra = 1

    def get_queryset(self, request):
        return super(LangLocaleAdmin, self).get_queryset(request).prefetch_related('lang')


class LangForm(forms.ModelForm):
    def clean_code(self):
        return self.cleaned_data['code'].upper()

    class Meta:
        model = models.Lang
        exclude = ()


# class LangForm


class LangAdmin(admin.ModelAdmin):
    inlines = [LangLocaleAdmin]
    list_display = ("str", "default",)
    list_display_links = list_display

    form = LangForm

    def get_view_on_site_url(self, obj=None):
        if not obj:
            return None
        return urlresolvers.reverse("{}_preview".format(settings.PORTAL_DEFAULT_REDIRECT_VIEW),
                                    kwargs=dict(lang=obj.code.lower()))

        # def get_view_on_site_url


# class LangAdmin


class MainMenuI18nForm(admin.TabularInline):
    model = models.MainMenuI18n

    def get_queryset(self, request):
        return super(MainMenuI18nForm, self). \
            get_queryset(request).prefetch_related('menu', 'locale')


class MenuItemForm(admin.TabularInline):
    model = models.MenuItem

    def get_queryset(self, request):
        return super(MenuItemForm, self). \
            get_queryset(request).prefetch_related('menu')


class MenuItemI18nForm(admin.TabularInline):
    model = models.MenuItemI18n

    def get_queryset(self, request):
        return super(MenuItemI18nForm, self).\
            get_queryset(request).prefetch_related('menu_item', 'locale', 'menu_item__menu')


class MainMenuAdmin(admin.ModelAdmin):
    inlines = (MainMenuI18nForm, MenuItemForm, MenuItemI18nForm,)

    list_display = ("caption", "order", "hidden")
    list_display_links = list_display


# class MainMenuAdmin




def action(*args, **kwargs):
    pass


admin.site.register(models.Lang, LangAdmin)
admin.site.register(models.MainMenu, MainMenuAdmin)
admin.site.add_action(action, name="action")
admin.site.add_action(action, name="delete_selected")
