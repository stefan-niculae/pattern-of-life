import mgrs

coords_converter = mgrs.MGRS()


def latlon2mgrs(coords: tuple) -> str:
    return coords_converter.toMGRS(*coords).decode()


def mgrs2latlon(coords: str) -> tuple:
    return coords_converter.toLatLon(str.encode(coords))
