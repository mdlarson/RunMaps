'''Process Strava FIT files to GPX files.'''
import logging
import warnings
from fit2gpx import StravaConverter

# set up logging
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore", category=UserWarning)


def convert_fit_to_gpx(input_dir, output_dir):
    '''Convert Strava FIT files to GPX format.'''
    logging.info("Starting FIT → GPX conversion...")
    # 1. Create StravaConverter object
    # dir_in must be path to central unzipped Strava bulk export folder
    # specify dir_out if desired, defaults to 'activities_gpx'
    strava_conv = StravaConverter(dir_in=input_dir, dir_out=output_dir)

    # 2. Unzip the files
    logging.info("Unzipping files...")
    strava_conv.unzip_activities()

    # 3. Add metadata to GPX
    logging.info("Adding metadata...")
    strava_conv.add_metadata_to_gpx()

    # 4. Convert to GPX
    logging.info("Converting files...")
    strava_conv.strava_fit_to_gpx()

    logging.info("Conversion complete.")


if __name__ == '__main__':
    # Define input/output directories
    DIR_STRAVA = 'data'
    OUTPUT_DIR = 'data/activities_gpx'

    # Run conversion process
    convert_fit_to_gpx(DIR_STRAVA, OUTPUT_DIR)
