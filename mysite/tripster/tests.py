from django.test import Client
import time

# Create your tests here.
c = Client()
response = c.post('/', {'username':'madoka', 'password':'a'})
print response.status_code
response = c.get('/feed')
print response.content
