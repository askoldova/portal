from django.db import models
from django.utils.translation import ugettext_lazy as _


class Generation(models.Model):
    class Meta:
        managed = False
        verbose_name = _("Generation")
        verbose_name_plural = _("Generation")