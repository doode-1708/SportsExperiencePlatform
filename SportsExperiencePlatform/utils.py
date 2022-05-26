import numpy as np


def haversine_vectorized(df,
                         user_lat="user_latitude",
                         user_lon="user_longitude",
                         event_lat="event_latitude",
                         event_lon="event_longitude"):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).
        Vectorized version of the haversine distance for pandas df
        Computes distance in kms
    """

    lat_1_rad, lon_1_rad = np.radians(df[user_lat].astype(float)),\
        np.radians(df[user_lon].astype(float))
    lat_2_rad, lon_2_rad = np.radians(df[event_lat].astype(float)),\
        np.radians(df[event_lon].astype(float))
    dlon = lon_2_rad - lon_1_rad
    dlat = lat_2_rad - lat_1_rad

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) *\
        np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c
