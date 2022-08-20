from typing import List

from pydantic import BaseModel


class CategoryAddSchema(BaseModel):
    ids: List[int]
