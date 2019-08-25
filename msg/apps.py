from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MsgConfig(AppConfig):
    name = 'msg'
    verbose_name = _('Messaging System')
