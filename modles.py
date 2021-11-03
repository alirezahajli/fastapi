from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from .database import Base






class SearchQuery(Base):

    __tablename__ = "query"


    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)

    owner = relationship("Url", back_populates="owner")


class Url(Base):

    __tablename__ = "urls"


    id = Column(Integer, primary_key=True, index=True)
    Url = Column(String, unique=True, index=True)
    description = Column(String)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("urls.id"))

    items = relationship("SearchQuery", back_populates="urls")




