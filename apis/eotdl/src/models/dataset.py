from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List

from .validators import validate_name


class Version(BaseModel):
    version_id: int
    createdAt: datetime = datetime.now()
    size: int = 0


class Dataset(BaseModel):
    uid: str
    id: str
    name: str
    authors: List[str]
    source: str
    license: str
    files: str
    versions: List[Version] = []
    description: str = ""
    tags: List[str] = []
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    likes: int = 0
    downloads: int = 0
    quality: int = 0

    @field_validator("name")
    def check_name_is_valid(cls, name):
        if name is not None:
            assert validate_name(name) == name
        return name

    @field_validator("source")
    def check_source_is_url(cls, source):
        if source != "" and source is not None:
            if not source.startswith("http") and not source.startswith("https"):
                raise ValueError("source must be a valid url")
        return source


class STACDataset(BaseModel):
    uid: str
    id: str
    name: str
    description: str = ""
    tags: List[str] = []
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()
    likes: int = 0
    downloads: int = 0
    quality: int = 1
    size: int = 0
    catalog: dict = {}
    versions: List[Version] = []

    # @validator("name")
    # def check_name_is_valid(cls, name):
    #     if name is not None:
    #         assert validate_name(name) == name
    #     return name
