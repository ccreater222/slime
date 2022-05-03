from types import FunctionType
from logging import basicConfig

class ExceptionDecorator:
    def __init__(self, name="default", handler=None, logger=None) -> None:
        self.name = name
        if handler == None:
            self.handler = self.defaultExceptionHandler
        else:
            self.handler = handler
        if logger == None:
            self.logger = basicConfig()
        else:
            self.logger = logger
    def __call__(self, function) -> FunctionType:
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                return result
            except Exception as e:
                self.handleException(e)
        return wrapper
    def handleException(self, e: Exception) -> None:
        self.handler(e)
    def defaultExceptionHandler(self, e: Exception) -> None:
        print(f"found exeception {self.name}")
        print(e)
