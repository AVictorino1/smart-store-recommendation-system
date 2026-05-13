class NotFoundError(Exception):
    def __init__(self, message="Product Not Found", details=None):
        super().__init__(message)
        self.status_code = 404
        self.error_code = "NOT_FOUND"
        self.details=details


class BadRequest(Exception):
    def __init__(self, message="Bad Request", details=None):
        super().__init__(message)
        self.status_code = 400
        self.error_code = "BAD_REQUEST"
        self.details=details