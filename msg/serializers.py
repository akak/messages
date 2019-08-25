from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers

from .models import Message


class MsgSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        kwargs['child'].fields.pop('message')
        return serializers.ListSerializer(*args, **kwargs)

    class Meta:
        model = Message
        fields = ['created', 'sender', 'receiver', 'subject', 'message', ]
        read_only_fields = ['created']

    def validate_sender(self, value):
        if self.context['request'].user != value:
            raise exceptions.PermissionDenied(_("can't create message!"))
        return value
