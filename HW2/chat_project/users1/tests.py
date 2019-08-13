
from django.test import TestCase
from django.test import Client
from users1.models import Users

class CreateUserTest(TestCase):

    def test_valid_signup(self):
        c = Client()
        response = c.post(
            '/item/Signup/',
            {
                'firstname': 'Sara',
                'lastname': 'Sabori',
                'number_of_friends': 10,
                'birthday': '2019-06-01',
                'username': 'Sara' ,
                'password' : '125#@'
            }
        )
        self.assertEqual(response.status_code, 200)

        u = Users.objects.get(firstname= 'Sara')
        self.assertEqual(u.lastname, 'Sabori')

    def test_invalid_signup(self):
        c = Client()
        response = c.post(
            '/item/Signup/',
            {
                'firstname': 'Sara',
                'lastname': 'Sabori',
                'number_of_friends': 'salam',
                'username': 'Sara' ,
                'password' : '125#@'
            }
        )
        self.assertEqual(response.status_code, 200)