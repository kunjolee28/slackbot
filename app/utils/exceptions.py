class BadRequest(Exception):
    """Bad Request Exception"""
    code = 400
    status = 'bad request'

class Unauthorized(Exception):
    """Unauthorized Exception"""
    code = 401
    status = 'unauthorized'
 
class Forbidden(Exception):
    """Forbidden Exception"""
    code = 403
    status = 'forbidden'
  
class InternalServerError(Exception):
    """Internal Server Error Exception"""
    code = 500
    status = 'internal server error'


class BadGateway(Exception):
    """Bad Gateway Exception"""
    code = 502
    status = 'bad gateway'
