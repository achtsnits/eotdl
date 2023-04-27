import { PUBLIC_EOTDL_API } from '$env/static/public';
import retrieveTags from '$lib/tags/retrieveTags';
import retrieveLikedDatasets from '$lib/datasets/retrieveLikedDatasets';

export const load = async ({params, fetch, parent}) => {
	const data = await parent()
	const url = `${PUBLIC_EOTDL_API}/datasets?name=${params.name}`;
	const res = await fetch(url)
	const dataset = await res.json();
	const tags = await retrieveTags(fetch)
	let liked_datasets = []
	if (data.user)
		liked_datasets = await retrieveLikedDatasets(fetch, data.id_token)
	if (res.status == 200) 
		return { dataset, tags, liked_datasets: liked_datasets.map(d => d.id), name: params.name };
	return { error: data.detail };
}

export const prerender = false;