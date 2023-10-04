from rest_framework.exceptions import APIException


class SubdomainIsAlreadyUsed(APIException):
    status_code = 404
    text = "Multilanding domain is not available"
    x_code = 'x001'
    
    
class IncorrectSubDomain(APIException):
    status_code = 400
    text = "Incorrect sub domain value"
    x_code = 'x002'