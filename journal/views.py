from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Post
from .serializers import EventSerializer, PostSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_fields = {
        'name': ['icontains', ],
        'remark': ['icontains', ],
    }
    ordering_fields = ('name',)
    ordering = ('name',)
    pagination_class = None


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filter_fields = {
        'performances__event__name': ['icontains', ],
    }
    ordering_fields = ('workout_date',)
    ordering = ('-workout_date',)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
