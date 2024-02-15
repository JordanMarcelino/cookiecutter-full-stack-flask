from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from pydantic import BaseModel

T = TypeVar("T")


# Response information
class Info(BaseModel):
    success: bool
    meta: Optional[Dict[str, Any]]
    message: str


# Standard web response
class WebResponse(Generic[T], BaseModel):
    info: Info
    data: Optional[Union[List[T], T]]
