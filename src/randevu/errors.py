from contextlib import contextmanager
from functools import wraps
import logging
import traceback
from rest_framework.response import Response

from typing import Tuple


logger = logging.getLogger(__name__)


class AppBaseException(BaseException):
    """Base User Exception"""
    def __init__(self, text, x_code='', status_code=404):
        self.x_code = x_code
        self.text = text
        self.status_code = status_code


def safe_api(func):
    def _wrap(*args, **kwargs):
        try:
            reply = func(*args, **kwargs)
            return reply
        except AppBaseException as exc:
            logger.error(traceback.format_exc())
            return Response(data={
                'errors': [ { 'text': exc.text, 'code': exc.x_code } ]
            }, status=exc.status_code)
        except Exception as exc:
            logger.error(traceback.format_exc())
            return Response(data={
                'errors': [ { 'text': str(exc), 'code': 'null' } ]
            }, status=404)

    return _wrap


def safe_run(exceptions = (Exception, )):
    def retry(function):
        @wraps(function)
        def _retry(*args, **kwargs):
            try:
                reply = function(*args, **kwargs)
                return reply
            except exceptions + (Exception, ) as exc:
                return Response(data={
                    'errors': [
                        {
                            'text': str(exc),
                            'code': 'x'
                        }
                    ]
                }, status=400)
            except Exception as exc:
                return Response(data={
                    'errors': [
                        {
                            'text': str(exc),
                            'code': 'x'
                        }
                    ]
                }, status=400)
        return _retry
    return retry