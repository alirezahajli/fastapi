from sqlalchemy.orm import Session
from sqlalchemy import and_


import models, schemas


def url_exist(db: Session, url_owner_id: int, url_link: str):

    if (
        db.query(models.Url)
        .filter(and_(models.Url.owner_id == url_owner_id, models.Url.link == url_link))
        .first()
    ):
        return True
    return False


def get_url_by_title(db: Session, title: str):

    return db.query(models.Url).filter(models.Url.title == title).first()


def get_url_by_link(db: Session, link: str):

    return db.query(models.Url).filter(models.Url.link == link).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Url).offset(skip).limit(limit).all()


def create_url(db: Session, url: schemas.UrlCreate):

    db_url = models.Url(
        link=url["link"],
        title=url["title"],
        descreption=url["descreption"],
        owner_id=url["owner_id"],
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_search_queries(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.SearchQuery).offset(skip).limit(limit).all()


def get_search_query_by_query(db: Session, search_query_query: str):

    return (
        db.query(models.SearchQuery)
        .filter(models.SearchQuery.query == search_query_query)
        .first()
    )


def create_search_query(db: Session, search_query: schemas.QueryCreate):
    db_search_query = models.SearchQuery(query=search_query.query)
    db.add(db_search_query)
    db.commit()
    db.refresh(db_search_query)
    return db_search_query
