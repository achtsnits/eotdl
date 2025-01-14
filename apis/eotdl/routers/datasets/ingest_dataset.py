from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends, File, Form, UploadFile
import logging
from pydantic import BaseModel
from typing import Optional

from ..auth import get_current_user
from ...src.models import User
from ...src.usecases.datasets import (
    ingest_file,
    ingest_existing_file,
)  # , ingest_stac, ingest_file_url

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/{dataset_id}")
async def ingest(
    dataset_id: str,
    file: Optional[UploadFile] = File(None),
    version: int = Form(),  # debería quitarlo (un file solo se puede subir a la última versión si no está ya)
    parent: str = Form(None),  # debería quitarlo (sacarlo del nombre?)
    checksum: str = Form(None),  # optional bc browser
    filename: str = Form(None),
    fileversion: int = Form(None),
    user: User = Depends(get_current_user),
):
    try:
        if filename:
            assert not file, "File provided as both file and filename"
            assert not parent, "Parent provided as both parent and filename"
            assert fileversion, "Fileversion not provided"
            dataset_id, dataset_name, file_name = await ingest_existing_file(
                filename, dataset_id, fileversion, version, checksum, user
            )
        else:
            if file.size > 1000000000:  # 1GB
                raise Exception(
                    "File too large, please use the CLI to upload large files."
                )
            dataset_id, dataset_name, file_name = await ingest_file(
                file, dataset_id, version, parent, checksum, user
            )
        return {
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "file_name": file_name,
        }
    except Exception as e:
        logger.exception("datasets:ingest")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# class IngestSTACBody(BaseModel):
#     stac: dict  # json as string


# @router.put("/stac/{dataset_id}")
# async def ingest_stac_catalog(
#     dataset_id: str,
#     body: IngestSTACBody,
#     user: User = Depends(get_current_user),
# ):
#     try:
#         return ingest_stac(body.stac, dataset_id, user)
#     except Exception as e:
#         logger.exception("datasets:ingest_url")
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

# class IngestURLBody(BaseModel):
#     url: str


# @router.post("/{dataset_id}/url")
# async def ingest_url(
#     dataset_id: str,
#     body: IngestURLBody,
#     user: User = Depends(get_current_user),
# ):
#     # try:
#     dataset_id, dataset_name, file_name = await ingest_file_url(
#         body.url, dataset_id, user
#     )
#     return {
#         "dataset_id": dataset_id,
#         "dataset_name": dataset_name,
#         "file_name": file_name,
#     }
#     # except Exception as e:
#     #     logger.exception("datasets:ingest")
#     #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
