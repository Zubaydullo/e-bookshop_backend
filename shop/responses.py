from rest_framework.response import Response
from rest_framework import status


class ResponseFail(Response):
    def __init__(self, data=""):
        data = {"code": 200, "error":True, "status": "fail", "result": data}
        self.__init__ = super().__init__(data, status=200)


class ResponseSuccess(Response):
    def __init__(self, data="", filter_fields=None):
        if isinstance(data, Response):
            data = data.data

        data = {"code":200, "error":False, "status": "success", "result": data}
        if filter_fields:
            data["filter_fields"] = filter_fields
        super().__init__(data, status=200)
