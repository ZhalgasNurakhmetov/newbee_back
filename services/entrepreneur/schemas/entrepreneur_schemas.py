from typing import List

from pydantic import BaseModel


class EntrepreneurAddPhotoSchema(BaseModel):
    video: str
    photoList: List[str]
