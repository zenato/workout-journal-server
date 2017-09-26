import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Event, Post, Performance


class UserNode(DjangoObjectType):
    class Meta:
        model = User


class PostNode(DjangoObjectType):
    class Meta:
        model = Post


class PerformanceNode(DjangoObjectType):
    class Meta:
        model = Performance


class EventNode(DjangoObjectType):
    last_performance = graphene.Field(PerformanceNode, source='last_performance')

    class Meta:
        model = Event


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode)

    events = graphene.List(EventNode, name=graphene.String())
    event = graphene.Field(EventNode, id=graphene.ID(required=True))

    posts = graphene.List(PostNode, name=graphene.String())
    post = graphene.Field(PostNode, id=graphene.ID(required=True))

    def resolve_user(self, info):
        return User.objects.get(pk=info.context.user.id)

    def resolve_events(self, info, name=None):
        where = {'owner': info.context.user, }
        if name:
            where['name__contains'] = name
        return Event.objects.filter(**where)

    def resolve_event(self, info, id=None):
        return Event.objects.get(owner=info.context.user, pk=id)

    def resolve_posts(self, info, name=None):
        where = {'owner': info.context.user, }
        if name:
            where['performances__event__name'] = name
        return Post.objects.filter(**where)

    def resolve_post(self, info, id=None):
        return Post.objects.get(owner=info.context.user, pk=id)
