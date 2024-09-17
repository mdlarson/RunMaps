'''Process GPX files to draw image of each day's routes.'''
import logging
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import gpxpy


# Set up logging
logging.basicConfig(level=logging.INFO)


def downsample_lat_lon(latitudes, longitudes, N=10):
    '''Downsample GPS data for faster processing.'''
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    # keep every Nth point
    logging.info("Downsampling GPS points for file.")
    return latitudes[::N], longitudes[::N]


def get_lat_lon_points(file_path):
    '''Extract lat and long from GPX file.'''
    latitudes, longitudes = [], []
    with open(file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)
    return downsample_lat_lon(latitudes, longitudes)


def plot_routes_for_date(date, gpx_files, output_folder):
    '''Plot all routes for a given date and save image.'''
    png_files = []

    try:
        plt.figure(figsize=(10, 10))

        for gpx_file in gpx_files:
            logging.info("Drawing route for %s.", gpx_file)
            latitudes, longitudes = get_lat_lon_points(gpx_file)
            plt.plot(longitudes, latitudes, marker='o',
                     linestyle='-', color='orange', markersize=10, linewidth=10)

        # style preferences
        plt.axis(False)  # disable axis and labels
        plt.gca().set_facecolor('none')  # transparent background
        plt.grid(False)

        # save image for the date
        output_file = os.path.join(output_folder, f'{date}.png')
        plt.savefig(output_file, format='png', transparent=True,
                    bbox_inches='tight', pad_inches=0)

        png_files.append(output_file)
        plt.clf()
        plt.close()
    finally:
        plt.close('all')  # close all plots in case of error
    return png_files


def group_gpx_files_by_date(input_dir):
    '''Group GPX files by date they were recorded.'''
    gpx_files_by_date = defaultdict(list)  # dict of lists of files

    # Iterate through all GPX files
    for filename in os.listdir(input_dir):
        if filename.endswith(".gpx"):
            file_path = os.path.join(input_dir, filename)
            timestamp = get_first_timestamp(file_path)
            if timestamp:
                date_str = timestamp.date()  # only need date
                logging.info("Adding %s to list.", date_str)
                gpx_files_by_date[date_str].append(file_path)
    return gpx_files_by_date


def get_first_timestamp(file_path):
    '''Extract date of first timestamp in GPX file.'''
    with open(file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                if segment.points:
                    return segment.points[0].time  # return datetime object
    return None  # if no points are found


if __name__ == '__main__':
    # Define input/output directories
    GPX_DIR = 'data/activities_gpx'
    OUTPUT_DIR = 'output'

    grouped_files = group_gpx_files_by_date(GPX_DIR)

    for date, files in grouped_files.items():
        logging.info("Drawing route images for %s...", date)
        plot_routes_for_date(date, files, OUTPUT_DIR)
        logging.info("Route image for %s complete.", date)
