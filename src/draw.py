from mpl_toolkits.basemap import Basemap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import fiona
from fiona.crs import to_string,from_epsg
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon, shape
from shapely.prepared import prep
from itertools import chain
from mpl_toolkits.basemap.pyproj import Proj, transform
'''
#Convert to lon/lat
fromproj = Proj(to_string(shp.crs))
toproj = Proj("+init=EPSG:4326")
coords=[]

pnyc = Proj(proj='lcc', datum='NAD83',lat_1=shp.crs['lat_1'],lat_2=shp.crs['lat_2'],lat_0=shp.crs['lat_0'],lon_0=shp.crs['lon_0'],
     x_0=shp.crs['x_0'],
     y_0=shp.crs['y_0'])
with fiona.open('data/CITY_LIMITES_GSP.shp', 'w', 'ESRI Shapefile', shp.schema.copy(), crs=from_epsg(4326)) as output:
    for point in shp[0]['geometry']['coordinates'][0][0]:
        coords.append(pnyc(point[0],point[1],inverse=True))
        print coords[-1]
    copy = dict(shp[0])
    copy['geometry']['coordinates']=[[coords]]
    output.write(copy)
'''
shp = fiona.open('data/CITY_LIMITS.shp')
lat_0 = shp.crs['lat_0']
lon_0 = shp.crs['lon_0']
shp.close()
shp = fiona.open('data/SJ.shp')
extra = 0
bds = shp.bounds
ll = (bds[0], bds[1])
ur = (bds[2], bds[3])
coords = list(chain(ll, ur))
w, h = coords[2] - coords[0], coords[3] - coords[1]
m = Basemap(
    projection='tmerc',
    lon_0=-121.848729129722,
    lat_0=37.3020714417266,
    ellps = 'WGS84',
    llcrnrlon=coords[0],
    llcrnrlat=coords[1],
    urcrnrlon=coords[2],
    urcrnrlat=coords[3],
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)
shp.close()
m.readshapefile('data/SJ','San Jose')
m.drawcoastlines() # draw coastlines
m.drawmapboundary() # draw a line around the map region
m.drawmapscale(
    coords[0] + 0.08, coords[1] + 0.015,
    coords[0], coords[1],
    10.,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555',
    fontcolor='#555555',
    zorder=5)
data = pd.read_excel('data/dumping_data.xlsx')
lat_loc = data['intersection_lat'].dropna()
lon_loc = data['intersection_lng'].dropna()
m.scatter(lon_loc.tolist(),
    lat_loc.tolist(),
    10, marker='o', lw=.25,
    facecolor='#33ccff', edgecolor='w',
    alpha=0.9, antialiased=True,
    label='Dumping Locations', zorder=3, latlon=True)
plt.show()
