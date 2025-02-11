from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routers.auth import (
    login,
    logout,
    me,
    token,
    update_user_data,
    credentials,
    accept_terms_and_conditions,
)
from .routers.tags import retrieve_tags
from .routers.datasets import (
    retrieve_dataset,
    create_dataset,
    ingest_dataset,
    download_dataset,
    update_dataset,
    # delete_dataset,
)
from .routers import admin, migrate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# auth
app.include_router(login.router, prefix="/auth")
app.include_router(logout.router, prefix="/auth")
app.include_router(me.router, prefix="/auth")
app.include_router(token.router, prefix="/auth")
app.include_router(update_user_data.router, prefix="/auth")
app.include_router(credentials.router, prefix="/auth")
app.include_router(accept_terms_and_conditions.router, prefix="/auth")
# tags
app.include_router(retrieve_tags.router, prefix="/tags")
# dataset
app.include_router(retrieve_dataset.router, prefix="/datasets")
app.include_router(create_dataset.router, prefix="/datasets")
app.include_router(ingest_dataset.router, prefix="/datasets")
app.include_router(download_dataset.router, prefix="/datasets")
app.include_router(update_dataset.router, prefix="/datasets")
# # app.include_router(upload_large_files.router, prefix="/datasets")
# app.include_router(delete_dataset.router, prefix="/datasets")
# other
app.include_router(admin.router)
app.include_router(migrate.router)

logging.basicConfig(
    filename="/tmp/eotdl-api.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

VERSION = "2023.10.17"


@app.get("/", name="home", include_in_schema=False)
async def root():
    return {
        "name": "eotdl",
        "version": VERSION,
        "description": "Earth Observation Training Data Lab",
        "contact": "support@eotdl.com",
    }
