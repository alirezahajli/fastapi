from typing import List, Optional

from pydantic import BaseModel


class UrlBase(BaseModel):
    id: int
    descreption: Optional[str] = None
    title: str
    link: str
    owner_id: int
    

class Url(UrlBase):
    id: int

    class Config:
        orm_mode = True


class SearchQueryBase(BaseModel):
    query: str
    

class SearchQueryCreate(SearchQueryBase):
   query: str


class SearchQuery(SearchQueryBase):
    id: int
    urls: List[Url] = []

    class Config:
        orm_mode = True
