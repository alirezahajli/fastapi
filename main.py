from typing import List
import logging

import schemas
from googlesearch import FetchGoogleSearchResult
from database import engine, init_db, get_session

import elasticapm
from fastapi import Depends, FastAPI, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import selectinload
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.handler import LogstashFormatter


logger = logging.getLogger("logstash")
logger.setLevel(logging.INFO)


handler = AsynchronousLogstashHandler(
    host="192.168.107.32",
    port=5000,
    database_path="",
)

formatter = LogstashFormatter()
handler.setFormatter(formatter)


logger.addHandler(handler)


NOTFOUND = "Query Not Found"
EXIST = "Query Already Exist."

app = FastAPI()


apm = make_apm_client(
    {
        "SERVICE_NAME": "sub-app-test",
        "SERVER_URL": "http://192.168.107.32:8200",
        "CAPTURE_BODY": "all",
    }
)

app.add_middleware(ElasticAPM, client=apm)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def test():
    logger.warning("????")

    elasticapm.set_custom_context({"message": "??? ?????"})
    elasticapm.set_user_context(username="root", email="root@mail.com", user_id=1)
    return {"message": "Welcome"}


@app.get("/search_queries/", response_model=List[schemas.QueryReadWithUrl])
async def read_search_queries(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    queries = await session.execute(
        select(schemas.Query)
        .options(selectinload(schemas.Query.urls))
        .offset(offset)
        .limit(limit)
    )
    queries = queries.scalars().all()

    return queries


@app.get("/search_queries/{query_name}", response_model=schemas.QueryReadWithUrl)
async def read_search_queries_with_query(
    *,
    session: AsyncSession = Depends(get_session),
    query_name: str,
):

    query = await session.execute(
        select(schemas.Query)
        .where(schemas.Query.query == query_name)
        .options(selectinload(schemas.Query.urls))
    )
    query = query.scalars().all()

    if not query:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    return query[0]


@app.post("/search_queries/", response_model=schemas.QueryRead)
async def create_query(
    *,
    session: AsyncSession = Depends(get_session),
    query: schemas.QueryCreate,
    background_task: BackgroundTasks,
):
    query_exist = await session.execute(
        select(schemas.Query).where(schemas.Query.query == query.query)
    )
    query_exist = query_exist.scalars().first()
    if query_exist:
        raise HTTPException(status_code=404, detail=EXIST)
    db_query = schemas.Query.from_orm(query)
    session.add(db_query)
    await session.commit()
    await session.refresh(db_query)
    background_task.add_task(get_google_search_result, db_query)

    return db_query


async def get_google_search_result(query):

    crawler = FetchGoogleSearchResult(query.query, 1)
    crawled_data = crawler.fetch
    logger.info(f" crawled_data : {crawled_data}")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            for data in crawled_data:
                if data != None:
                    db_url = schemas.Url(
                        description=crawled_data[data]["description"],
                        title=crawled_data[data]["title"],
                        link=crawled_data[data]["link"],
                        query_id=query.id,
                    )
                    session.add(db_url)
                logger.info(f" {query.query} : Urls inserted in")
            session.commit()


@app.get("/urls/", response_model=List[schemas.UrlRead])
async def read_search_queries(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    urls = await session.execute(select(schemas.Url).offset(offset).limit(limit))
    urls = urls.scalars().all()
    return urls


@app.delete("/search_queries/{query_id}")
async def delete_urls_and_query(
    *, session: AsyncSession = Depends(get_session), query_id: int
):
    urls = await session.execute(
        select(schemas.Url).where(schemas.Url.query_id == query_id)
    )
    urls = urls.scalars().all()
    for url in urls:
        await session.delete(url)
    query = await session.get(schemas.Query, query_id)

    if not query:
        raise HTTPException(status_code=404, detail=NOTFOUND)
    await session.delete(query)
    await session.commit()

    return {"deleted": True}


@app.delete("/delete_queries/{query_name}")
async def delete_urls_and_query(
    *, session: AsyncSession = Depends(get_session), query_name: str
):

    query = await session.execute(
        select(schemas.Query).where(schemas.Query.query == query_name)
    )
    query = query.scalars().first()
    if not query:
        raise HTTPException(status_code=404, detail=NOTFOUND)

    urls = await session.execute(
        select(schemas.Url).where(schemas.Url.query_id == query.id)
    )
    urls = urls.scalars().all()
    for url in urls:
        await session.delete(url)

    await session.delete(query)
    await session.commit()

    return {"deleted": True}


@app.get("/users/", response_model=List[schemas.UserOut])
async def read_search_queries(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = await session.execute(select(schemas.User).offset(offset).limit(limit))
    users = users.scalars().all()
    return users
