import graphene
import graphene.types.datetime
from .schema import EventNode, PostNode
from .models import Event, Post, Performance


# Event mutations

class EventInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    unit = graphene.String(required=True)
    value = graphene.Int()
    remark = graphene.String()


class CreateEvent(graphene.Mutation):
    class Arguments:
        data = EventInput(required=True)

    event = graphene.Field(EventNode)

    @staticmethod
    def mutate(root, info, data=None):
        event = Event(owner=info.context.user, **data)
        event.save()
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        data = EventInput(required=True)

    event = graphene.Field(EventNode)

    @staticmethod
    def mutate(root, info, id=None, data=None):
        Event.objects.filter(pk=id, owner=info.context.user).update(**data)
        event = Event.objects.get(pk=id)
        return UpdateEvent(event=event)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id=None):
        event = Event.objects.get(pk=id, owner=info.context.user)
        event.delete()
        return DeleteEvent(success=True)


# Post mutations

class PostInput(graphene.InputObjectType):
    workout_date = graphene.types.datetime.DateTime()
    remark = graphene.String()


class PerformanceInput(graphene.InputObjectType):
    event = graphene.Int()
    value = graphene.Int(required=True)
    set1 = graphene.Int()
    set2 = graphene.Int()
    set3 = graphene.Int()
    set4 = graphene.Int()
    set5 = graphene.Int()


class CreatePost(graphene.Mutation):
    class Arguments:
        data = PostInput(required=True)
        performances = graphene.List(PerformanceInput)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, data=None, performances=[]):
        post = Post(owner=info.context.user, **data)
        post.save()

        for performance_data in performances:
            event_id = performance_data.pop('event')
            event = Event.objects.get(pk=event_id)

            performance = Performance.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        data = PostInput(required=True)
        performances = graphene.List(PerformanceInput)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, id=None, data=None, performances=[]):
        Post.objects.filter(pk=id, owner=info.context.user).update(**data)
        post = Post.objects.get(pk=id, owner=info.context.user)

        Performance.objects.filter(post=post).delete()

        for performance_data in performances:
            event_id = performance_data.pop('event')
            event = Event.objects.get(pk=event_id)

            performance = Performance.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id=None):
        post = Post.objects.get(pk=id, owner=info.context.user)
        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()