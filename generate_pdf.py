'''Lay out images in grid and generate PDF.'''
import logging
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import draw_routes


# Set up logging
logging.basicConfig(level=logging.INFO)


def draw_calendar_with_routes(output_pdf, grouped_files):
    '''Lay out routes in a calendar grid and save as PDF.'''
    # set up canvas, margins, and grid
    c = canvas.Canvas(output_pdf, pagesize=(11 * inch, 78 * inch))
    margin = 0.25 * inch
    cell_width = 1.5 * inch
    cell_height = 1.5 * inch

    y_start = (78 * inch) - margin - cell_height  # Start after the top margin

    # determine year and find first day
    year = min(grouped_files.keys()).year
    for week_num in range(1, 53):
        for day_of_week in range(7):  # Sun = 0, Sat = 6
            week_start = datetime.strptime(
                f"{year} {week_num} {day_of_week}", "%Y %W %w").date()

            if week_start in grouped_files:
                png_files = grouped_files[week_start]

                for png_file in png_files:
                    try:
                        img_reader = ImageReader(png_file)
                        img_width, img_height = img_reader.getSize()  # find original size

                        # calculate scale to fit image
                        scale_x = cell_width / img_width
                        scale_y = cell_height / img_height
                        scale_factor = min(scale_x, scale_y)

                        # calculate scaled image size
                        new_width = img_width * scale_factor
                        new_height = img_height * scale_factor

                        # center image in cell
                        x = margin + (day_of_week * cell_width) + \
                            (cell_width - new_width) / 2
                        y = y_start - (week_num * cell_height)

                        c.drawImage(img_reader, x, y,
                                    width=new_width, height=new_height)

                    except Exception as e:
                        logging.error("Error processing %s: %s", png_file, e)
    c.save()


if __name__ == '__main__':
    INPUT_FILES = draw_routes.group_gpx_files_by_date('data/activities_gpx')

    OUTPUT_PDF = 'route-calendar.pdf'
    draw_calendar_with_routes(OUTPUT_PDF, INPUT_FILES)
