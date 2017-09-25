import graphene
from django.test import TestCase
from graphene.test import Client
from .models import User, Event, Post, Performance
from .schema import Query
from .mutation import Mutation


class MockContext(object):
    def __init__(self, user):
        self.user = user


class TestQuery(Query, graphene.ObjectType):
    pass


class TestMutation(Mutation, graphene.ObjectType):
    pass


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()

        cls.user = User.objects.get(pk=1)
        cls.schema = graphene.Schema(query=TestQuery, mutation=TestMutation)


# Event

class EventTests(BaseTestCase):
    def create(self):
        event = Event(
            name='test',
            unit='kg',
            value=10,
            remark='test-remark',
            owner=self.user,
        )
        event.save()
        self.event = event

    """
    Ensure we can get a event objects.
    """

    def test_query_events(self):
        self.create()
        client = Client(self.schema)
        executed = client.execute(
            '''
            query {
                allEvents(name: "test") { name }
            }
            ''',
            context_value=MockContext(self.user),
        )
        self.assertTrue(len(executed.get('data')) > 0)

    """
    Ensure we can get a event object.
    """

    def test_query_event(self):
        self.create()
        client = Client(self.schema)
        executed = client.execute(
            '''
            query {
                event(id: %s) { name }
            }
            ''' % self.event.id,
            context_value=MockContext(self.user),
        )
        event = executed.get('data').get('event')
        self.assertIsNotNone(event)

    """
    Ensure we can create event
    """

    def test_create_event(self):
        client = Client(self.schema)
        executed = client.execute(
            '''
            mutation {
              createEvent(data: {name: "test", unit: "KG", value: 10, remark: "test-remark"}) {
                event {
                  id
                }
              }
            }
            ''',
            context_value=MockContext(self.user),
        )
        event = executed.get("data").get('createEvent').get("event")
        self.assertIsNotNone(event)


# Post

class PostTests(BaseTestCase):
    def create(self):
        event = Event(
            name='test',
            unit='kg',
            value=10,
            remark='test-remark',
            owner=self.user,
        )
        event.save()

        post = Post(
            owner=self.user,
        )
        post.save()

        Performance(
            post=post,
            event=event,
            value=10,
            set1=1,
            set2=2,
            set3=3,
            set4=4,
            set5=5,
        ).save()

        self.post = post

    """
    Ensure we can get a post objects.
    """

    def test_query_posts(self):
        self.create()
        client = Client(self.schema)
        executed = client.execute(
            '''
                query {
                    allPosts(name: "test") {
                        performances {
                            id
                            event {
                                name
                            }
                        }
                    }
                }
            ''',
            context_value=MockContext(self.user),
        )
        self.assertTrue(len(executed.get('data')) > 0)

    """
    Ensure we can get a post object.
    """

    def test_query_post(self):
        self.create()
        client = Client(self.schema)
        executed = client.execute(
            '''
                query {
                    post(id: %s) {
                        workoutDate
                        performances {
                            id
                            event {
                                name
                            }
                        }
                    }
                }
            ''' % self.post.id,
            context_value=MockContext(self.user),
        )
        post = executed.get('data').get('post')
        self.assertIsNotNone(post)

    """
    Ensure we can create event
    """

    def test_create_post(self):
        client = Client(self.schema)
        executed = client.execute(
            '''
            mutation {
              createPost(
                data: { workoutDate: "2017-01-10T21:33:15.233Z", remark: "latest" },
                performances: [{ event: 17, value: 20, set1: 10 }, { event: 48, value: 10, set1: 20 }]
              ) {
                post {
                  id
                  workoutDate
                  remark
                  performances {
                    event {
                      name
                    }
                    value
                    set1
                  }
                }
              }
            }
            ''',
            context_value=MockContext(self.user),
        )
        post = executed.get("data").get('createPost').get("post")
        self.assertIsNotNone(post)
