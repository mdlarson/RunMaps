'''Process GPX files to draw routes.'''
import gpxpy
import matplotlib.pyplot as plt

# Read GPX file
with open('data/activities_gpx/9282480094.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extra lat/long
latitudes = []
longitudes = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            latitudes.append(point.latitude)
            longitudes.append(point.longitude)

# Plot the track
plt.figure(figsize=(10, 10))
plt.axis(False)  # disable axis and labels
plt.gca().set_facecolor('none')  # transparent background
plt.plot(longitudes, latitudes, marker='o',
         linestyle='-', color='orange', markersize=3)
# plt.title('GPS Track')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
plt.grid(False)
plt.savefig('output/gps_track.svg', format='svg', transparent=True,
            bbox_inches='tight', pad_inches=0)
plt.show()
