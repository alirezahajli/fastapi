from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, query

import crud, models, schemas
from googlesearch import FetchGoogleSearchResult
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/urls/", response_model=schemas.Url)
def create_url(url: schemas.UrlBase, db: Session = Depends(get_db)):
    db_user = crud.get_url_by_link(db, link=url.link)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_url(db=db, url=url)


@app.get("/search_queries/", response_model=List[schemas.SearchQuery])
def read_search_queries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urls = crud.get_search_queries(db, skip=skip, limit=limit)
    return urls


@app.get("/urls/{url_id}", response_model=schemas.Url)
def read_url(url_id: int, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_id(db, url_id=url_id)
    if db_url is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return db_url


# @app.post("/search_queries/{url_id}/urls/", response_model=schemas.SearchQuery)
# def create_urls_for_query(
#     url_id: int, url: schemas.Url, db: Session = Depends(get_db)
# ):
#     return crud.create_url(db=db, url=url, url_id=url_id)


@app.post("/search_queries/", response_model=schemas.SearchQuery)
def create_search_query(
    search_query: schemas.SearchQueryCreate, db: Session = Depends(get_db)
):
    db_search_query = crud.get_search_query_by_query(
        db, search_query_query=search_query.query
    )
    if db_search_query:
        raise HTTPException(status_code=400, detail="query already entered")

    last_search_queries_created = crud.create_search_query(
        db=db, search_query=search_query
    )

    crawler = FetchGoogleSearchResult(search_query.query, 1)
    crawled_data = crawler.fetch
    for data in crawled_data:

        crawled_data[data]["owner_id"] = last_search_queries_created.id
        db_user = crud.get_url_by_link(db, link=crawled_data[data]["link"])
        if db_user:
            raise HTTPException(status_code=400, detail="url already entered")
        crud.create_url(db=db, url=crawled_data[data])

    return last_search_queries_created


@app.get("/urls/", response_model=List[schemas.Url])
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urls = crud.get_urls(db, skip=skip, limit=limit)
    return urls
