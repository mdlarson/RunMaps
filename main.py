'''Convert Strava FIT files to GPX, draw the routes as images, and output a PDF.'''
from convert_fit_to_gpx import convert_fit_to_gpx
from draw_routes import group_gpx_files_by_date, plot_routes_for_date
from generate_pdf import draw_calendar_with_routes


def main():
    '''Convert Strava FIT files to GPX, draw the routes as images, and output a PDF.'''
    # 1. Convert FIT files to GPX
    # dir_strava = 'data'
    dir_gpx = 'data/activities_gpx'
    # convert_fit_to_gpx(dir_strava, dir_gpx)

    # 2. Group GPX files by date and draw images
    grouped_files = group_gpx_files_by_date(dir_gpx)
    dir_img = 'output'

    img_files_grouped_by_date = {}
    for date, files in grouped_files.items():
        img_files = plot_routes_for_date(date, files, dir_img)
        img_files_grouped_by_date[date] = img_files

    # 3. Create PDF from images
    year = 2024
    output_pdf = f'route-calendar-{2024}.pdf'
    draw_calendar_with_routes(output_pdf, dir_img, year)


if __name__ == '__main__':
    main()
