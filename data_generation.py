import pandas as pd
import numpy as np


""" Parameters """
n_points = 100

centers = [
    (34.799858, 68.478098),
    (35.016225, 65.570469),
    (33.352490, 65.164307),
]
location_std = .5

count_mean = 15
count_std  = 4

demographics = ['men', 'women', 'children']
armed_per = .8


""" Generation """
lats = np.concatenate([np.random.normal(c[0], location_std, size=n_points) for c in centers])
lons = np.concatenate([np.random.normal(c[1], location_std, size=n_points) for c in centers])

np.random.shuffle(lats)
np.random.shuffle(lons)

desc = np.random.choice(demographics, size=n_points)

armed = np.random.choice([False, True], size=n_points, p=[1-armed_per, armed_per])
armed[desc != 'men'] = False  # only men can be armed

counts = np.random.normal(count_mean, count_std, size=n_points).astype(int)
counts[counts <= 0] = 1
counts[~armed] = counts[~armed] * 5


""" Put together """
expected = pd.DataFrame(dict(
    lat=lats[:n_points],
    lon=lons[:n_points],
    persons=counts,
    desc=desc,
    armed=armed,
))
