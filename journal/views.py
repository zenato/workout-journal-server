from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsOwner
from .models import Event, Post
from .serializers import EventSerializer, PostSerializer


class EventList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_fields = {
        'name': ['icontains', ],
        'remark': ['icontains', ],
    }
    ordering_fields = ('name',)
    ordering = ('name',)
    pagination_class = None

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_fields = {
        'performances__event__name': ['icontains', ],
    }
    ordering_fields = ('workout_date',)
    ordering = ('-workout_date',)

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
