from django.core.cache import cache
from django.shortcuts import render
import requests


def say_hello(request):
    key = 'httpbit_result'
    if cache.get(key) is None:
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        cache.set(key, data)
    
    return render(request, 'hello.html', {'name': cache.get(key)})
