from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import RequestsClient
from rest_framework.test import APIRequestFactory
from . import models

client = RequestsClient()
factory = APIRequestFactory()

def test_get_courses():
    response = client.get('http://127.0.0.1:8000/courses/')
    assert response.status_code == 200, 'get request failed'

def test_post_users():
    # response = client.post(
    #     'http://127.0.0.1:8000/users/', 
    #     {'username': 'Alex', 'password': '12345', 'status': 'student'}
    # )
    request = factory.post(
        'http://127.0.0.1:8000/users/',
        {'username': 'Alex', 'password': '12345', 'status': 'student'},
        format='json'
    )
    print(request, dir(request), sep='\n')
    # assert response.status_code == 200, 'post user failed'

    user = models.User.objects.get(username='Alex')
    print(user)
    assert user != None, 'user was not written to the database'


tests = (test_get_courses, test_post_users)
for test in tests:
    test()