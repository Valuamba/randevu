
from randevu.errors import AppBaseException


class UserException(AppBaseException):
    """Base User Exception"""
    
    
class UserVerificationFailed(UserException):
    x_code = 'x003'
    
    
# class UserRecoveryFailed(UserException):
#     x_