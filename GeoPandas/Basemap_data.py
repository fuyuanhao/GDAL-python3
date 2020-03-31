from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap()
map.bluemarble()
#map.drawmapboundary(fill_color='aqua')
#map.fillcontinents(color='#cc9955', lake_color='aqua')
map.drawcountries()
map.drawrivers(color='#0000ff')
plt.show()

map = Basemap(projection='ortho',
              lat_0=33, lon_0=100)
#Fill the globe with a blue color
map.drawmapboundary(fill_color='blue')
#Fill the continents with the land color
map.fillcontinents(color='green',lake_color='blue')
map.drawcoastlines()
plt.show()