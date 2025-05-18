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
    print(date_start, date_end)

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


value = get_value_at_location(
    bands=[
        # "CO",
        # "HCHO",
        # "NO2",
        # "O3",
        "SO2",
        "CH4",
        "AER_AI_340_380",
        "AER_AI_354_388",
    ],
    date="2025-05-18",
    lon=41.03143,
    lat=21.33474,
)

print("Values:", value)
# air_quality = {
#     "CO": 0.0253452931841214,
#     "HCHO": 2.406330546970518e-05,
#     "NO2": 1.3021036617525777e-05,
#     "O3": 0.1237474158406257,
#     "SO2": 0.1237474158406257,
#     "AER_AI_340_380": 1.3089114427566528,
#     "AER_AI_354_388": 1.6423608660697937,
# }
# user_info = {
#     "id": 1,
#     "date_of_birth": "2001-03-01",
#     "height": 180,
#     "weight": 75,
#     "illnesses": "Hyperthyroidism, Arhytmia",
#     "allergies": "None",
#     "addictions": "Alcohol, Cigarettes, Recreative drugs",
#     "family_history": "Cancer, Heart Disease",
# }
