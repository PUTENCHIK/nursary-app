from fastapi import HTTPException


class MyHTTPException(HTTPException):
    def __init__(self, detail: str):
        self.code = 404

        super(MyHTTPException, self).__init__(status_code=self.code, detail=detail)

    @staticmethod
    def http(detail: str):
        return HTTPException(status_code=404, detail=detail)
