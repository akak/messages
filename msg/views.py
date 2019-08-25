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
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.PermissionDenied("Unauthenticated!")
        qs = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created')
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
