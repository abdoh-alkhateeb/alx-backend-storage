#!/usr/bin/env python3
"""
Defines `Cache` class.
"""

import redis
import uuid
import functools

from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """
    Counts calls.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores call history.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))

        outputs = method(self, *args, **kwargs)

        self._redis.rpush(f"{method.__qualname__}:outputs", outputs)

        return outputs

    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls.
    """
    r = redis.Redis()
    name = method.__qualname__
    count = int((r.get(name) or bytes()).decode())

    print(f"{name} was called {count} times:")

    for inputs, output in zip(
        r.lrange(f"{name}:inputs", 0, -1), r.lrange(f"{name}:outputs", 0, -1)
    ):
        print(f"{name}(*{inputs.decode()}) -> {output.decode()}")


class Cache:
    """
    Blueprint for cache instances.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key and stores a value using it.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        Gets data using a given key and converts it to desired type if needed.
        """
        data = self._redis.get(key)
        if fn is None:
            return data
        return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Returns a stored value as a string if exists.
        """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """
        Returns a stored value as a integer if exists.
        """
        return self.get(key, int)
