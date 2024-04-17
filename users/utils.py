# utils.py
from rest_framework import status
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if 'user_not_found' in str(exc):
            response.status_code = status.HTTP_404_NOT_FOUND
        elif 'incorrect_password' in str(exc):
            response.status_code = status.HTTP_401_UNAUTHORIZED

    return response