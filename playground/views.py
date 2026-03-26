from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        message = EmailMessage('subject', 'message', 'dima@gmail.com', ['dimos@gmail.com'])
        message.attach_file('playground/static/images/phos.png')
        message.send()
    except BadHeaderError:
        pass

    return render(request, 'hello.html', {'name': 'Mosh'})
