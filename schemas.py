from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class UrlBase(SQLModel):
    description: Optional[str] = None
    title: str
    link: str
    query_id: Optional[int] = Field(default=None, foreign_key="query.id")


class Url(UrlBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    query: Optional["Query"] = Relationship(back_populates="urls")


class UrlCreate(UrlBase):
    pass


class UrlRead(UrlBase):
    id: int


class UrlUpdate(SQLModel):
    id: Optional[int] = None
    description: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None


class QueryBase(SQLModel):
    query: str


class Query(QueryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    urls: List["Url"] = Relationship(back_populates="query")


class QueryRead(QueryBase):
    id: int


class QueryCreate(QueryBase):
    pass


class QueryUpdate(SQLModel):
    query: Optional[str] = None


class UrlReadWithQuery(UrlRead):
    query: Optional[QueryRead] = None


class QueryReadWithUrl(QueryRead):
    urls: List[UrlRead] = []
