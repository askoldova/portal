from django import forms
from django.contrib import admin

from . import models
from portal import generators


class LangLocaleAdmin(admin.TabularInline):
    model = models.LangLocale
    fk_name = 'lang'
    extra = 1


class LangForm(forms.ModelForm):
    def clean(self):
        self.cleaned_data['code'] = self.cleaned_data['code'].upper()

    def save(self, commit=True):
        res = super(LangForm, self).save(commit)

        generators.accept_and_generate(generators.IndexPageGenerate())
        generators.accept_and_generate(generators.DefaultPageGenerate(self.cleaned_data['code'].lower()))

        return res

    class Meta:
        model = models.Lang
        exclude = ()

# class LangForm


class LangAdmin(admin.ModelAdmin):
    inlines = [LangLocaleAdmin]
    list_display = ("str", "default",)
    list_display_links = list_display

    form = LangForm
# class LangAdmin


class MainMenuI18nForm(admin.TabularInline):
    model = models.MainMenuI18n

class MenuItemForm(admin.TabularInline):
    model = models.MenuItem

class MenuItemI18nForm(admin.TabularInline):
    model = models.MenuItemI18n

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