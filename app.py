from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query

import schemas
from googlesearch import FetchGoogleSearchResult
from database import SessionLocal, engine

from sqlmodel import SQLModel, select, Session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_google_search_result(query):
    crawler = FetchGoogleSearchResult(query.query, 1)
    crawled_data = crawler.fetch
    with Session(engine) as session:
        for data in crawled_data:
            if data != None:

                db_url = schemas.Url(
                    description=crawled_data[data]["description"],
                    title=crawled_data[data]["title"],
                    link=crawled_data[data]["link"],
                    query_id=query.id,
                )
                session.add(db_url)
        session.commit()


@app.get("/search_queries/", response_model=List[schemas.QueryReadWithUrl])
def read_search_queries(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    queries = session.exec(select(schemas.Query).offset(offset).limit(limit)).all()
    return queries


@app.get("/search_queries/{query_name}", response_model=schemas.QueryReadWithUrl)
def read_search_queries_with_query(
    *,
    session: Session = Depends(get_session),
    query_name: str,
):

    query_exist = session.get(schemas.Query, query_name)
    if not query_exist:
        raise HTTPException(status_code=404, detail="Query not found")
    query = session.exec(
        select(schemas.Query).where(schemas.Query.query == query_name)
    ).first()
    return query


@app.post("/search_queries/", response_model=schemas.QueryRead)
def create_query(
    *,
    session: Session = Depends(get_session),
    query: schemas.QueryCreate,
):
    statement = select(schemas.Query).where(schemas.Query.query == query.query)
    query_exist = session.exec(statement).first()
    if query_exist:
        raise HTTPException(status_code=404, detail="Query already exist.")
    db_query = schemas.Query.from_orm(query)
    session.add(db_query)
    session.commit()
    session.refresh(db_query)
    get_google_search_result(db_query)

    return db_query


@app.get("/urls/", response_model=List[schemas.UrlRead])
def read_search_queries(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    urls = session.exec(select(schemas.Url).offset(offset).limit(limit)).all()
    return urls


@app.delete("/search_queries/{query_id}")
def delete_urls_and_query(*, session: Session = Depends(get_session), query_id: int):
    urls = session.exec(
        select(schemas.Url).where(schemas.Url.query_id == query_id)
    ).all()
    for url in urls:
        session.delete(url)
    query = session.get(schemas.Query, query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    session.delete(query)
    session.commit()

    return {"deleted": True}
