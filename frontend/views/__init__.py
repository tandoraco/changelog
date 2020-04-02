from django.shortcuts import render
from rest_framework import status


def error_handler(request, status_code, context):
    return render(request, 'error_handler.html', context=context, status=status_code)


def handler404(request, *args, **argv):
    context = {
        'status_code_description': '404 - Not Found',
        'error_details': 'Sorry, an error has occurred, Requested page not found!'
    }
    return error_handler(request, status.HTTP_404_NOT_FOUND, context)


def handler500(request, *args, **argv):
    context = {
        'status_code_description': '500 - Server Error',
        'error_details': 'Sorry, an error has occurred and our engineers are notified. '
                         'We will resolve it as soon as possible.'
    }
    return error_handler(request, status.HTTP_500_INTERNAL_SERVER_ERROR, context)
