import graphene
import graphene.types.datetime
from .schema import EventNode, PostNode
from .models import Event, Post, Performance


# Event mutations

class EventFields:
    name = graphene.String(required=True)
    unit = graphene.String(required=True)
    value = graphene.Int(required=True)
    remark = graphene.String()


class CreateEventInput(graphene.InputObjectType, EventFields):
    pass


class CreateEvent(graphene.Mutation):
    class Arguments:
        input = CreateEventInput(required=True)

    event = graphene.Field(EventNode)

    @staticmethod
    def mutate(root, info, input=None):
        event = Event(owner=info.context.user, **input)
        event.save()
        return CreateEvent(event=event)


class UpdateEventInput(graphene.InputObjectType, EventFields):
    id = graphene.ID(required=True)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        input = UpdateEventInput(required=True)

    event = graphene.Field(EventNode)

    @staticmethod
    def mutate(root, info, input=None):
        id = input.get('id')
        Event.objects.filter(pk=id, owner=info.context.user).update(**input)
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

class PerformanceEventInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class PerformanceInput(graphene.InputObjectType):
    event = graphene.InputField(PerformanceEventInput, required=True)
    value = graphene.Int(required=True)
    set1 = graphene.Int()
    set2 = graphene.Int()
    set3 = graphene.Int()
    set4 = graphene.Int()
    set5 = graphene.Int()


class PostFields:
    workout_date = graphene.types.datetime.DateTime()
    remark = graphene.String()
    performances = graphene.List(PerformanceInput)


class CreatePostInput(graphene.InputObjectType, PostFields):
    pass


class CreatePost(graphene.Mutation):
    class Arguments:
        input = CreatePostInput(required=True)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, input=None):
        performances = input.pop('performances')

        post = Post(owner=info.context.user, **input)
        post.save()

        for performance_data in performances:
            event_data = performance_data.pop('event')
            event = Event.objects.get(pk=event_data.get('id'))
            performance = Performance.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return CreatePost(post=post)


class UpdatePostInput(graphene.InputObjectType, PostFields):
    id = graphene.ID(required=True)


class UpdatePost(graphene.Mutation):
    class Arguments:
        input = UpdatePostInput(required=True)

    post = graphene.Field(PostNode)

    @staticmethod
    def mutate(root, info, input=None):
        id = input.get('id')
        performances = input.pop('performances')
        Performance.objects.filter(post__pk=id).delete()

        Post.objects.filter(pk=id, owner=info.context.user).update(**input)
        post = Post.objects.get(pk=id, owner=info.context.user)

        for performance_data in performances:
            event_data = performance_data.pop('event')
            event = Event.objects.get(pk=event_data.get('id'))
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
