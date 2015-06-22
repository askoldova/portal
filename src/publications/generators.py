from _celery.celery import app
from . import gen_events, views
import generation

publications_service = views.publications_service

@app.task(name="portal.generators._generate_internal")
def _generate_internal(command1):
    accept_and_generate(command1)


def apply_internal(command):
    _generate_internal.apply_async((command,))
# def apply_internal


def generate_page(command):
    """
    Generate and save publication item
    :param command: publications.gen_gen_events.PublicationPageGenerate
    :return:
    """
    publication = publications_service.get_publication_by_id(command.publication_id)
    generation.save_generation(generation.GenerationResult(
        views.url_of_publication(command.publication_id),
        views.generate_publication(command.publication_id)
    ))


def accept_and_generate(command):
    """
    :param command:
    :return:
    """
    if isinstance(command, gen_events.PublicationPageGenerate):
        generate_page(command)
        return True

    return False  # default return - command can't be handled by
# def accept_and_generate
