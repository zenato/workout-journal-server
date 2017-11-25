import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User as UserModel
from .models import Event as EventModel, Post as PostModel, Performance as PerformanceModel


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Post(DjangoObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node,)
        filter_fields = {
            'performances__event__name': ['icontains'],
        }

    @classmethod
    def get_node(cls, info, id):
        return PostModel.objects.get(pk=id, owner=info.context.user.id)


class Performance(DjangoObjectType):
    class Meta:
        model = PerformanceModel


class Event(DjangoObjectType):
    last_performance = graphene.Field(Performance, source='last_performance')

    class Meta:
        model = EventModel
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'icontains'],
        }

    @classmethod
    def get_node(cls, info, id):
        return EventModel.objects.get(pk=id, owner=info.context.user.id)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    user = graphene.Field(User)
    events = DjangoFilterConnectionField(Event)
    posts = DjangoFilterConnectionField(Post)

    def resolve_user(self, info):
        return UserModel.objects.get(pk=info.context.user.id)

    def resolve_events(self, info, **args):
        return EventModel.objects.filter(owner=info.context.user).order_by('-pk')

    def resolve_posts(self, info, **args):
        return PostModel.objects.filter(owner=info.context.user).order_by('-pk')
