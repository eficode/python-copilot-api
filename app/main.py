from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute

from db.db import create_db_and_tables
from routes import books, authors

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Cleanup code can be added here if needed

app = FastAPI(lifespan=lifespan,
              generate_unique_id_function=custom_generate_unique_id)

router = APIRouter()
router.include_router(books.router)
router.include_router(authors.router)

app.include_router(router)