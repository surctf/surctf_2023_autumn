from typing import Union

from pydantic import BaseModel


class UglyJSONRequest(BaseModel):
    ugly_json: str


class PrettyJSONResponse(BaseModel):
    pretty_json: str
