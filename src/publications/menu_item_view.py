from django.contrib.auth.decorators import login_required
from django.core import urlresolvers

import core

menu_item_url = r'^{}(?P<lang_code>\w\w)/(?P<menu_item_id>\d+)/?$'
menu_item_page_url = r'^{}(?P<lang_code>\w\w)/(?P<menu_item_id>\d+)/(?P<page>\d+).html$'


def url_of_menu_item(lang_code, menu_item_id):
    core.check_exist_and_type(lang_code, "lang_code", str, unicode)
    core.check_exist_and_type(menu_item_id, "menu_item_id", long, int)

    return urlresolvers.reverse(menu_item_view, kwargs=dict(lang_code=lang_code, menu_item_id=menu_item_id))


def url_of_menu_item_admin(lang_code, menu_item_id):
    core.check_exist_and_type(lang_code, "lang_code", str, unicode)
    core.check_exist_and_type(menu_item_id, "menu_item_id", long, int)

    return urlresolvers.reverse(menu_item_view_admin, kwargs=dict(lang=lang_code, menu_item_id=menu_item_id))


def menu_item_view(request, lang_code, menu_item_id):
    pass


menu_item_view_admin = login_required(menu_item_view)


def url_of_menu_item_page(lang_code, menu_item_id, page):
    core.check_exist_and_type(lang_code, "lang_code", str, unicode)
    core.check_exist_and_type(menu_item_id, "menu_item_id", long, int)
    core.check_exist_and_type(page, "page", long, int)

    return urlresolvers.reverse(menu_item_view_page, kwargs=dict(lang=lang_code, menu_item_id=menu_item_id, page=page))


def menu_item_view_page(request, lang_code, menu_item_id, page):
    pass


menu_item_view_page_admin = login_required(menu_item_view_page)
