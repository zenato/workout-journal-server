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


class Query(graphene.ObjectType):
    all_events = graphene.List(EventNode, name=graphene.String())
    all_posts = graphene.List(PostNode, name=graphene.String())

    def resolve_all_events(self, info, name=None):
        where = {
            'owner': info.context.user,
        }

        if name:
            where['name__contains'] = name

        items = Event.objects.filter(**where)
        return items

    def resolve_all_posts(self, info, name=None):
        where = {
            'owner': info.context.user,
        }

        if name:
            where['performances__event__name'] = name

        items = Post.objects.filter(**where)
        return items
