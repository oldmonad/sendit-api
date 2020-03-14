import json

from django.core.cache import cache
from rest_framework import exceptions


def cache_data(key, data):
    try:
        cache.set(key, json.dumps(data), 300)
    except Exception:
        raise exceptions.APIException("Something went wrong with redis")

    return True


def retrieve_cached_data(key):
    try:
        data = json.loads(cache.get(key))
    except Exception:
        raise exceptions.APIException("Something went wrong with redis")

    return data


def delete_cached_data(key):
    try:
        cache.delete(key)
    except Exception:
        raise exceptions.APIException("Something went wrong with redis")

    return True
