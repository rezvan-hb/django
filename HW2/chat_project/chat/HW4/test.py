
from django.test import TestCase
from django.test import Client
from users1.models import Users

class CreateUserTest(TestCase):

    def test_valid_message(self):
        c = Client()
        response = c.get(
            '/chatitem/message/',
            {
                'conversation_id': 1,
                'from_date': ''
                'to_date': ''
                'size': 5
            }
        )
        self.assertEqual(response.status_code, 200)
                                           
    def test_invalid_message(self):
        c = Client()
        response = c.post(
            '/chatitem/message/',
            {
                conversation_id = 1,
                sender_id = 1 ,
                message = 'salam'
            }
        )
        self.assertEqual(response.status_code, 200)