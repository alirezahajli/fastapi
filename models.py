from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from database import Base






class SearchQuery(Base):

    __tablename__ = "queries"


    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)

    owner = relationship("Url", back_populates="urls")


class Url(Base):

    __tablename__ = "urls"


    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, unique=True, index=True)
    descreption = Column(String)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("queries.id"))

    urls = relationship("SearchQuery", back_populates="owner")




