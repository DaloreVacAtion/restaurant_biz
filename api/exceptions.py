from rest_framework.exceptions import APIException


class NotExistException(APIException):
    status_code = 404
    default_detail = 'requested data not found'


class BadRequest(APIException):
    status_code = 400
    default_detail = ''


class ServerError(APIException):
    status_code = 500
    default_detail = 'internal server error'
