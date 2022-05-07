
from argparse import ArgumentError
from typing import Any


class Response:
    success: bool
    def toDict(self):
        data = {}
        for k in self.get_need_attr():
            val = getattr(self, k, None)
            if val == None:
                raise ArgumentError()
            data[k] = val
        return data
    def get_need_attr(self):
        result = []
        bases = getattr(self.__class__, '__bases__', None)
        if bases == None:
            bases = []
        else:
            bases = list(bases)
        bases.append(self)
        for base in bases:
            keys = getattr(base, '__annotations__', {})
            result += keys.keys()
        return list(set(result))

class SuccessResponse(Response):
    success = True
    data: Any
    total: int
    size: int
    currentpage: int
    page: int
    def __init__(self,data, total,size,currentpage,page) -> None:
        self.data = data
        self.total = total
        self.size = size
        self.currentpage = currentpage
        self.page = page

class FailedResponse(Response):
    success = False
    msg: str