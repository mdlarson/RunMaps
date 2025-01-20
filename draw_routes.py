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
    '''Plot all routes for a given date and save square images without distortion.'''
    png_files = []

    try:
        # Create a new figure
        fig, ax = plt.subplots()

        all_latitudes, all_longitudes = [], []
        for gpx_file in gpx_files:
            logging.info("Drawing route for %s.", gpx_file)
            latitudes, longitudes = get_lat_lon_points(gpx_file)
            all_latitudes.extend(latitudes)
            all_longitudes.extend(longitudes)
            ax.plot(longitudes, latitudes, marker='o',
                    linestyle='-', color='orange', markersize=5, linewidth=2)

        # Ensure the aspect ratio is equal for true-to-life representation
        ax.set_aspect('equal', adjustable='datalim')

        # Add some padding around the plotted data
        if all_latitudes and all_longitudes:
            lat_margin = (max(all_latitudes) - min(all_latitudes)) * 0.1  # 10% margin
            lon_margin = (max(all_longitudes) - min(all_longitudes)) * 0.1  # 10% margin
            ax.set_xlim(min(all_longitudes) - lon_margin, max(all_longitudes) + lon_margin)
            ax.set_ylim(min(all_latitudes) - lat_margin, max(all_latitudes) + lat_margin)

        # Remove axes and background
        ax.axis(False)
        ax.set_facecolor('none')

        # Ensure the output is a square image
        fig.set_size_inches(10, 10)  # Force the figure to be square
        ax_position = ax.get_position()
        ax.set_position([0, 0, 1, 1])  # Make the plot fill the entire figure

        # Save the image as a square
        output_file = os.path.join(output_folder, f'{date}.png')
        fig.savefig(output_file, format='png', transparent=True,
                    bbox_inches='tight', pad_inches=0)
        png_files.append(output_file)

        plt.close(fig)
    except Exception as e:
        logging.error(f"Error processing routes for {date}: {e}")
    finally:
        plt.close('all')  # Ensure all plots are closed
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
