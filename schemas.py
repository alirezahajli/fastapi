from typing import List, Optional
from datetime import date, datetime
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class UserBase(SQLModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    password: str


class UserOut(SQLModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


class UrlBase(SQLModel):
    description: Optional[str] = None
    title: Optional[str] = None
    link: str
    query_id: Optional[int] = Field(default=None, foreign_key="query.id")


class Url(UrlBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    query: Optional["Query"] = Relationship(back_populates="urls")


class UrlCreate(UrlBase):
    pass


class UrlRead(UrlBase):
    id: int

    class Config:
        orm_mode = True


class QueryBase(SQLModel):
    query: str
    dated: Optional[datetime] = Field(default=datetime.now())


class Query(QueryBase, table=True):

    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)

    urls: List["Url"] = Relationship(back_populates="query")


class QueryRead(QueryBase):
    query: str
    # dated: Optional[datetime] = Field(default=datetime.now())
    class Config:
        orm_mode = True


class QueryCreate(QueryBase):
    pass


class QueryUpdate(SQLModel):
    query: Optional[str] = None


class UrlReadWithQuery(UrlRead):
    query: Optional[QueryRead] = None


class QueryReadWithUrl(QueryRead):
    urls: List[UrlRead] = []
