from django.test import TestCase
from django.test import Client
from .models import Student


class StudentTestCase(TestCase):

    def setUp(self):
        self.c = Client()

    def test_create(self):
        response = self.c.post('/opencmis/student/add/', {
            'first_name': 'Patrick',
            'last_name': 'Biggs',
            'date_of_birth': '12/03/2016',
            'gender': 'M',
            'ULN': '1232343454'},
            follow=True)

        self.assertEqual(response.status_code, 200)
