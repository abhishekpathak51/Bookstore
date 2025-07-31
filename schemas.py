from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    description: str
    author: str
    year: int


class BookCreate(BookBase):
    pass


# ✅ This class was missing!
class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2+
        # orm_mode = True         # for Pydantic v1.x
