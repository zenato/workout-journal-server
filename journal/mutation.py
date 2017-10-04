import graphene
import graphene.types.datetime
from graphene import relay
from .schema import Event, Post
from .models import Event as EventModel, Post as PostModel, Performance as PerformanceModel


# Event mutations

class EventFields:
    name = graphene.String(required=True)
    unit = graphene.String(required=True)
    value = graphene.Int(required=True)
    remark = graphene.String()


class CreateEvent(relay.ClientIDMutation):
    class Input(EventFields):
        pass

    event = graphene.Field(Event)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = EventModel(owner=info.context.user, **input)
        event.save()
        return CreateEvent(event=event)


class UpdateEvent(relay.ClientIDMutation):
    class Input(EventFields):
        id = graphene.ID(required=True)

    event = graphene.Field(Event)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        id = input.pop('id')
        EventModel.objects.filter(pk=id, owner=info.context.user).update(**input)
        event = EventModel.objects.get(pk=id)
        return UpdateEvent(event=event)


class DeleteEvent(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = EventModel.objects.get(pk=id, owner=info.context.user)
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


class CreatePost(relay.ClientIDMutation):
    class Input(PostFields):
        pass

    post = graphene.Field(Post)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        performances = input.pop('performances')

        post = PostModel(owner=info.context.user, **input)
        post.save()

        for performance_data in performances:
            event_data = performance_data.pop('event')
            event = EventModel.objects.get(pk=event_data.get('id'))
            performance = PerformanceModel.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return CreatePost(post=post)


class UpdatePost(relay.ClientIDMutation):
    class Input(PostFields):
        id = graphene.ID(required=True)

    post = graphene.Field(Post)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        id = input.pop('id')
        performances = input.pop('performances')
        PerformanceModel.objects.filter(post__pk=id).delete()

        PostModel.objects.filter(pk=id, owner=info.context.user).update(**input)
        post = PostModel.objects.get(pk=id, owner=info.context.user)

        for performance_data in performances:
            event_data = performance_data.pop('event')
            event = EventModel.objects.get(pk=event_data.get('id'))
            performance = PerformanceModel.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return UpdatePost(post=post)


class DeletePost(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        id = input.pop('id')
        post = PostModel.objects.get(pk=id, owner=info.context.user)
        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
