'''Process GPX files to draw SVG image of each day's routes.'''
import logging
import gpxpy
import os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


# Get date of workout
def get_first_timestamp(file_path):
    '''Find the date the workout started.'''
    with open(file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                if segment.points:
                    first_point = segment.points[0]
                    return first_point.time  # return datetime object
    return None  # if no points are found


def group_gpx_files_by_date(gpx_folder):
    '''Find GPX files recorded on the same date.'''
    gpx_files_by_date = defaultdict(list)  # dict of lists of files

    # Iterate through all GPX files
    for filename in os.listdir(gpx_folder):
        if filename.endswith(".gpx"):
            file_path = os.path.join(gpx_folder, filename)
            timestamp = get_first_timestamp(file_path)
            if timestamp:
                date_str = timestamp.date()  # only need date
                logging.info("Adding %s to list.", date_str)
                gpx_files_by_date[date_str].append(file_path)
    return gpx_files_by_date


def get_lat_lon_points(file_path):
    '''Extract lat and long from GPX.'''
    latitudes = []
    longitudes = []
    with open(file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        # extract lat/long
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)
    return latitudes, longitudes


def plot_routes_for_date(date, gpx_files, output_folder):
    '''Plot all routes for a given date.'''
    plt.figure(figsize=(10, 10))  # define plot

    for gpx_file in gpx_files:
        logging.info("Drawing SVG for %s.", gpx_file)
        # draw each route on the same plot
        latitudes, longitudes = get_lat_lon_points(gpx_file)
        plt.plot(longitudes, latitudes, marker='o',
                 linestyle='-', color='orange', markersize=3)

    # style preferences
    plt.axis(False)  # disable axis and labels
    plt.gca().set_facecolor('none')  # transparent background
    plt.grid(False)

    # save SVG for the date
    output_file = os.path.join(output_folder, f'{date}.svg')
    plt.savefig(output_file, format='svg', transparent=True,
                bbox_inches='tight', pad_inches=0)

    # clear plot for next date
    plt.clf()


# ====================
# CONFIG
# gpx_file_path = 'data/activities_gpx/9282480094.gpx'
gpx_folder = 'data/activities_gpx'
output_folder = 'output'


# LAUNCH
grouped_files = group_gpx_files_by_date(gpx_folder)
for date, files in grouped_files.items():
    # print(f"{date}: {files}")
    plot_routes_for_date(date, files, output_folder)

    logging.info("SVG for %s complete.", date)
