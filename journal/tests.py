import graphene
from django.test import TestCase
from graphene.test import Client
from .models import User
from .schema import Query
from .mutation import Mutation

TEST_USERNAME = 'zenato'


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

        cls.user = User.objects.get(username=TEST_USERNAME)
        cls.schema = graphene.Schema(query=TestQuery, mutation=TestMutation)


class EventTests(BaseTestCase):
    """
    Ensure we can get a event objects.
    """

    def test_query_event(self):
        client = Client(self.schema)
        executed = client.execute(
            '''
                query {
                    allEvents { name }
                }
            ''',
            context_value=MockContext(self.user)
        )
        self.assertIsNotNone(executed.get('data'))
