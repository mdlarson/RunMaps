'''Convert Strava FIT files to GPX, draw the routes as SVGs, and output a PDF.'''
from convert_fit_to_gpx import convert_fit_to_gpx
from draw_routes import group_gpx_files_by_date, plot_routes_for_date
from generate_pdf import draw_calendar_with_routes


def main():
    '''Convert Strava FIT files to GPX, draw the routes as SVGs, and output a PDF.'''
    # 1. Convert FIT files to GPX
    dir_strava = 'data'
    dir_gpx = 'data/activities_gpx'
    convert_fit_to_gpx(dir_strava, dir_gpx)

    # 2. Group GPX files by date and draw SVGs
    grouped_files = group_gpx_files_by_date(dir_gpx)
    dir_svg = 'output'

    svg_files_grouped_by_date = {}
    for date, files in grouped_files.items():
        svg_files = plot_routes_for_date(date, files, dir_svg)
        svg_files_grouped_by_date[date] = svg_files

    # 3. Create PDF from SVGs
    output_pdf = 'route-calendar.pdf'
    draw_calendar_with_routes(output_pdf, svg_files_grouped_by_date)


if __name__ == '__main__':
    main()
