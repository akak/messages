from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, verbose_name=_('sender'), on_delete=models.PROTECT, )
    receiver = models.ForeignKey(User, verbose_name=_('receiver'), on_delete=models.PROTECT, related_name='rcv')
    subject = models.CharField(max_length=50, verbose_name=_('subject'), )
    message = models.CharField(max_length=300, verbose_name=_('message'), null=True, blank=True, )
    created = models.DateField(db_index=True, verbose_name=_('create date'), auto_now_add=True, )
    unread = models.BooleanField(db_index=True, verbose_name=_('unread'), default=True, )

    def __str__(self):
        return f'{self.sender}->{self.receiver}:{self.subject}'

    class Meta:
        verbose_name = _('message')
