import graphene

from graphene_django.types import DjangoObjectType
from .models import Event, Post, Performance


class EventNode(DjangoObjectType):
    class Meta:
        model = Event


class PostNode(DjangoObjectType):
    class Meta:
        model = Post


class PerformanceNode(DjangoObjectType):
    class Meta:
        model = Performance


class Query(object):
    all_events = graphene.List(EventNode)
    all_posts = graphene.List(PostNode)

    def resolve_all_events(self, info):
        return Event.objects.filter(owner=info.context.user)

    def resolve_all_posts(self, info):
        return Post.objects.filter(owner=info.context.user)
