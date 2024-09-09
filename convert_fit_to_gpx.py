'''Process Strava FIT files to GPX files.'''
from fit2gpx import StravaConverter

DIR_STRAVA = 'data'

# 1. Create StravaConverter object
# dir_in must be path to central unzipped Strava bulk export folder
# specify dir_out if desired, defaults to 'activities_gpx'
strava_conv = StravaConverter(dir_in=DIR_STRAVA)

# 2. Unzip the files
strava_conv.unzip_activities()

# 3. Add metadata to GPX
strava_conv.add_metadata_to_gpx()

# 4. Convert to GPX
strava_conv.strava_fit_to_gpx()
