from rest_framework import status
from rest_framework.response import Response
import functools


def check_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def check_agent(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.agent:
            return Response({'message': 'Unauthorized. Need Agent permission.'}, status=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper
