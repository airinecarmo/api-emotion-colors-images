from dataclasses import dataclass, is_dataclass, asdict
from enum import Enum
from pydantic import BaseModel
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, BaseModel):
#             return obj.dict()
#         if is_dataclass(obj):
#             return asdict(obj)
#         if isinstance(obj, Enum):
#             return obj.value
#         return JSONEncoder.default(self, obj)


class Origin(Enum):
    SMART_BANK = 'SMART_BANK'


class ErrorResponse(BaseModel):
    code: int = None
    origin: Enum = Origin.SMART_BANK
    message: str = None


def build_response(status_code: int, content=None, json=None):
    if json:
        return JSONResponse(status_code=status_code, content=jsonable_encoder(json))
    if content:
        return JSONResponse(status_code=status_code, content=content)
    else:
        return JSONResponse(status_code=status_code)


def build_error_response(status_code: int, content=None):
    if content:
        error_response = ErrorResponse(code=status_code, message=content)
        return JSONResponse(status_code=status_code, content=jsonable_encoder(error_response))
    else:
        return JSONResponse(status_code=status_code)
