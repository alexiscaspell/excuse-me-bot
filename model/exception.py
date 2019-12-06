class AppException(Exception):
    def __init__(self, http_status=500, code='ERROR_APP', message=''):
        self.message = message
        self.http_status = http_status
        self.code = code

    def generate_response(self):
        return {"error": self.message, "code": self.code}, self.http_status