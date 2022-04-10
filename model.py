# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# Base = declarative_base()


# class Url(Base):
#     __tablename__ = "url"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     description = Column(String)
#     link = Column(String)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     query_id = Column(Integer, ForeignKey("query.id"))

#     author = relationship("Author")


# class Query(Base):
#     __tablename__ = "query"
#     id = Column(Integer, primary_key=True)
#     query = Column(String)
#     time_created = Column(DateTime(timezone=True), server_default=func.now())
#     time_updated = Column(DateTime(timezone=True), onupdate=func.now())
