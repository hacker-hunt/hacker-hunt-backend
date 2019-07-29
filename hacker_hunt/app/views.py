from django.shortcuts import render
from django.http import HttpResponse
import requests

def status(request):
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers={'Authorization': 'Token 9166bf03a80ed6b5ff8e55808532987e5d7cab7e'})
    status = response.json()
    print(status)
    return HttpResponse('Working')
