"""
Module for data engineering the sen12floods dataset
"""
from statistics import mean

import geopandas as gpd


def get_images_by_location(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Generate a GeoDataFrame with the available images for each location in the dataset. 

    :param gdf: GeoDataFrame generated from the ItemCollection of a sen12floods collection
    :return gdf_dates_per_aoi:  GeoDataFrame with the available images for each location in
                                the dataset.
            The returned GeoDataFrame has three columns:
                - location_id: the unique ID of each location.
                - images_count: the count of available images of each location.
                - images_dates: list with the dates of the available images of each location.
    """
    uniques_location_id = gdf['location_id'].unique()   # List of unique location ids
    uniques_location_id.sort()

    images_count_list, images_dates_list = [], []

    # Iterate the unique location ids, count the number of images per location and generate
    # a list with the dates of every image in a location
    for location_id in uniques_location_id:
        dates = gdf[gdf['location_id'] == location_id]['datetime']
        images_count_list.append(dates.count())
        images_dates_list.append(dates.tolist())

    data = {'sequence_id': uniques_location_id, 'dates_count': images_count_list, 'dates_list': images_dates_list}
    gdf_dates_per_aoi = gpd.GeoDataFrame.from_dict(data)

    return gdf_dates_per_aoi


def calculate_average_coordinates_distance(bounding_box_by_location: dict) -> list:
    """
    Calculate the mean distance between maximum and minixum longitude and latitude of the bounding boxes
    from the existing locations. This is intended to use these mean distance to generate the bounding 
    boxes of the new locations given a centroid.

    :param bounding_box_by_location: dictionary with format location_id : bounding_box for the existing
            locations in the sen12floods dataset.
    :return mean_long_diff, mean_lat_diff: mean longitude and latitude difference in the bounding boxes
    """
    long_diff_list, lat_diff_list = list(), list()

    for bbox in bounding_box_by_location.values():
        long_diff = bbox[2] - bbox[0]
        long_diff_list.append(long_diff)
        lat_diff = bbox[3] - bbox[1]
        lat_diff_list.append(lat_diff)

    mean_long_diff = mean(long_diff_list)
    mean_lat_diff = mean(lat_diff_list)

    return mean_long_diff, mean_lat_diff
