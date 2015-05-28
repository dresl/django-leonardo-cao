#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from filer.models import filemodels
from filer.utils.compatibility import python_2_unicode_compatible


@python_2_unicode_compatible
class Clipboard(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), verbose_name=_(
        'user'), related_name="filer_clipboards")
    files = models.ManyToManyField(
        'media.File', verbose_name=_('files'), related_name="in_clipboards",
        through='ClipboardItem')

    def append_file(self, file_obj):
        try:
            # We have to check if file is already in the clipboard as otherwise
            # polymorphic complains
            self.files.get(pk=file_obj.pk)
            return False
        except filemodels.File.DoesNotExist:
            newitem = ClipboardItem(file=file_obj, clipboard=self)
            newitem.save()
            return True

    def __str__(self):
        return "Clipboard %s of %s" % (self.id, self.user)

    class Meta:
        app_label = 'media'
        verbose_name = _('clipboard')
        verbose_name_plural = _('clipboards')


class ClipboardItem(models.Model):
    file = models.ForeignKey('media.File', verbose_name=_('file'))
    clipboard = models.ForeignKey(Clipboard, verbose_name=_('clipboard'))

    class Meta:
        app_label = 'media'
        verbose_name = _('clipboard item')
        verbose_name_plural = _('clipboard items')
