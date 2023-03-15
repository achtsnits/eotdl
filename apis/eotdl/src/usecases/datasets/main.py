from ...repos import DBRepo, OSRepo
from .IngestDataset	import IngestDataset
from .RetrieveDatasets import RetrieveDatasets
from .RetrieveOneDatasetByName import RetrieveOneDatasetByName
from .DownloadDataset import DownloadDataset
from .EditDataset import EditDataset
from ..tags import retrieve_tags

def ingest_dataset(file, name, description, user):
	db_repo = DBRepo()
	os_repo = OSRepo()
	ingest = IngestDataset(db_repo, os_repo)
	inputs = ingest.Inputs(name=name, file=file, uid=user.uid, description=description)
	outputs = ingest(inputs)
	return outputs.dataset

def retrieve_datasets():
	db_repo = DBRepo()
	retrieve = RetrieveDatasets(db_repo)
	inputs = retrieve.Inputs()
	outputs = retrieve(inputs)
	return outputs.datasets

def retrieve_dataset_by_name(name):
	db_repo = DBRepo()
	retrieve = RetrieveOneDatasetByName(db_repo)
	inputs = retrieve.Inputs(name=name)
	outputs = retrieve(inputs)
	return outputs.dataset

def download_dataset(id, user):
	db_repo = DBRepo()
	os_repo = OSRepo()
	retrieve = DownloadDataset(db_repo, os_repo)
	inputs = retrieve.Inputs(id=id)
	outputs = retrieve(inputs)
	return outputs.data_stream, outputs.object_info, outputs.name

def edit_dataset(id, name, description, tags, user):
	db_repo = DBRepo()
	edit = EditDataset(db_repo, retrieve_tags)
	inputs = edit.Inputs(id=id, name=name, description=description, tags=tags, uid=user.uid)
	outputs = edit(inputs)
	return outputs.dataset