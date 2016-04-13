from django.conf import settings

import generation as gen
import publications
from . import gen_events, views

publications_service = views.publications_service


def _generate_internal(command1):
    accept_and_generate(command1)


def apply_internal(command):
    if settings.PAGE_GENERATION_MODE == "local":
        accept_and_generate(command)
    elif settings.PAGE_GENERATION_MODE == "remote":
        _generate_internal.apply_async((command,))


# def apply_internal


def _generate_publication(command):
    """
    Generate and save publication item
    :param command: publications.gen_events.PublicationPageGenerate
    :return:
    """
    result = views.generate_publication_by_id(publication_id=command.publication_id)
    gen.save_generation(result)
    ref = publications.publications_view.publications_service.get_publication_ref_by_id(command.publication_id)
    if ref.old_id:
        apply_internal(gen_events.OldPublicationGenerate(old_id=ref.old_id, lang_code=ref.language.lower_code))


# def generate_publication

def _generate_all_pubs_default(command):
    """
    :type command: portal.gen_events.DefaultPageGenerate
    """
    gen.save_generation(
        views.generate_all_publications(
            views.url_of_all_publications(command.language_code), command.language_code))


# def generate_all_pubs_default

def _generate_old_publication(command):
    """
    :type command: publications.gen_events.OldPublicationGenerate
    """
    url = views.url_of_old_publication(command.lang_code, command.old_id)
    gen.save_generation(
        views.generate_old_publication(url=url, lang=command.lang_code, old_id=command.old_id)
    )


def accept_and_generate(command):
    """
    :param command:
    :return:
    """
    if isinstance(command, gen_events.DefaultPageGenerate):
        _generate_all_pubs_default(command)
        return True
    elif isinstance(command, gen_events.PublicationGenerate):
        _generate_publication(command)
        return True
    elif isinstance(command, gen_events.OldPublicationGenerate):
        _generate_old_publication(command)
        return True

    return False  # default return - command can't be handled by

# def accept_and_generate
