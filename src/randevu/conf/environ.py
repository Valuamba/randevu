"""Read .env file"""
import environ  # type: ignore
import os.path

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
    ENVIRONMENT=(str, 'QA')
)
if os.path.exists('randevu/.env'):
    environ.Env.read_env('randevu/.env')                  # reading .env file

__all__ = [
    'env',
]
