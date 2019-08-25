from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, mixins, viewsets

from .models import Message
from .serializers import MsgSerializer


class MsgViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = MsgSerializer

    def get_queryset(self):
        qs = Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)).order_by('-created')
        if 'unreadOnly' in self.request.GET:
            qs = qs.filter(unread=True)
        return qs

    def get_object(self):
        obj = super().get_object()
        if obj.unread:
            obj.unread = False
            obj.save()
        return obj

    def perform_destroy(self, instance):
        if instance.sender != self.request.user:
            raise exceptions.PermissionDenied(_("Can't delete other's messages!"))

        return super().perform_destroy(instance)
