import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import User
from . import views


class EventTests(APITestCase):
    def test_create_event(self):
        """
        Ensure we can create a new event object.
        """
        url = reverse('journal-events')
        data = {
            'name': 'name',
            'unit': 'unit',
            'value': 10,
            'remark': 'remark',
        }

        factory = APIRequestFactory()
        request = factory.post(url, data)

        user = User.objects.get(username='zenato')
        force_authenticate(request, user=user)

        view = views.EventList.as_view()
        response = view(request)
        response.render()

        result = json.loads(response.content)

        self.assertEqual(result['name'], 'name')
        self.assertEqual(result['unit'], 'unit')
        self.assertEqual(result['value'], 10)
        self.assertEqual(result['remark'], 'remark')

