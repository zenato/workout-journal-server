import json
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import User
from . import views

TEST_USERNAME = 'zenato'


class BaseTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        cls.factory = APIRequestFactory()
        cls.user = User.objects.get(username=TEST_USERNAME)

    def query(self, request, view):
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        return json.loads(response.content)


class EventTests(BaseTestCase):
    """
    Ensure we can create a new event object.
    """

    def test_create_event(self):
        request = self.factory.post('/events', {
            'name': 'name',
            'unit': 'unit',
            'value': 10,
            'remark': 'remark',
        })

        result = self.query(request, views.EventList.as_view())

        self.assertEqual(result['name'], 'name')
        self.assertEqual(result['unit'], 'unit')
        self.assertEqual(result['value'], 10)
        self.assertEqual(result['remark'], 'remark')

    """
    Ensure we can get event objects.
    """

    def test_list_event(self):
        request = self.factory.get('/events')
        result = self.query(request, views.EventList.as_view())

        self.assertTrue(len(result) > 0)
