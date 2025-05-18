import openeo, time, datetime, multiprocessing as mp

from Config.Common import get_from_env


def get_value_at_location(
    bands: str, date: str, lon: float, lat: float, radius_km: float = 5.0
) -> float:
    # Connect and authenticate
    connection = openeo.connect(
        "openeo.dataspace.copernicus.eu"
    ).authenticate_oidc_client_credentials(
        client_id=get_from_env("CDSE_CLIENT_ID"),
        client_secret=get_from_env("CDSE_CLIENT_SECRET"),
    )

    # Define 1-day time window
    date_start = (
        datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=1)
    ).strftime("%Y-%m-%d")
    date_end = (
        datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)
    ).strftime("%Y-%m-%d")

    # Convert radius to degrees (approx.)
    buffer_deg = radius_km / 111.0

    # Define small bounding box as polygon for aggregation
    spatial_geometry = {
        "type": "Polygon",
        "coordinates": [
            [
                [lon - buffer_deg, lat - buffer_deg],
                [lon + buffer_deg, lat - buffer_deg],
                [lon + buffer_deg, lat + buffer_deg],
                [lon - buffer_deg, lat + buffer_deg],
                [lon - buffer_deg, lat - buffer_deg],
            ]
        ],
    }
    ret = {}
    # Yes, I did try async. Yes, I did try multiprocessing. Yes, I got rate limited.
    for band in bands:
        time.sleep(1)
        cube = connection.load_collection(
            "SENTINEL_5P_L2",
            spatial_extent={
                "west": lon - buffer_deg,
                "east": lon + buffer_deg,
                "south": lat - buffer_deg,
                "north": lat + buffer_deg,
            },
            temporal_extent=[date_start, date_end],
            bands=[band],
        )

        # Reduce temporally first (1-day mean)
        cube = cube.reduce_dimension(dimension="t", reducer="mean")

        # Then aggregate spatially using the polygon
        vector_cube = cube.aggregate_spatial(
            geometries=spatial_geometry, reducer="mean"
        )

        # Execute and return value
        result = vector_cube.execute()
        if len(result) == 0:
            continue
        ret[band] = result[0][0]
    return ret