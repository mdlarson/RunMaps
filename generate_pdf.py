'''Lay out images in grid and generate PDF.'''
import os
import logging
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# Set up logging
logging.basicConfig(level=logging.INFO)


def draw_calendar_with_routes(output_pdf, png_directory, year_filter=None):
    '''Lay out routes by month in 3x4 grid with weekly rows, using dated filenames.'''
    c = canvas.Canvas(output_pdf, pagesize=(16 * inch, 20 * inch))
    outer_margin = .75 * inch  # space around border
    month_spacing = 0.25 * inch  # space between months

    # available space after outer margin and spacing
    # 3 columns, so 2 spaces between
    avail_width = 16 * inch - 2 * outer_margin - 2 * \
        month_spacing
    # 4 rows, so 3 spaces between
    avail_height = 20 * inch - 2 * outer_margin - 3 * \
        month_spacing

    # month block dimensions in 3x4 grid
    month_width = avail_width / 3
    month_height = avail_height / 4

    # cell dimensions
    cell_width = month_width / 7  # 7 days per week
    cell_height = month_height / 6  # 6 weeks per month to account for overflow

    # coordinates for each month in 3x4 grid
    month_coords = {
        1: (0, 0), 2: (1, 0), 3: (2, 0),  # Jan, Feb, Mar
        4: (0, 1), 5: (1, 1), 6: (2, 1),  # Apr, May, Jun
        7: (0, 2), 8: (1, 2), 9: (2, 2),  # Jul, Aug, Sep
        10: (0, 3), 11: (1, 3), 12: (2, 3)  # Oct, Nov, Dec
    }

    # loop through each image in directory
    for filename in os.listdir(png_directory):
        if filename.endswith('.png'):
            try:
                # extract date from filename
                date_str = os.path.splitext(filename)[0]  # '2023-05-18' part
                date = datetime.strptime(date_str, '%Y-%m-%d')

                # skip files not in specified year (if filter provided)
                if year_filter is not None and date.year != year_filter:
                    continue

                # get month, week of month, day of week
                month = date.month
                week_of_month = (date.day - 1) // 7
                day_of_week = date.weekday()  # 0 = Monday, 6 = Sunday (Python's default)

                # convert Python's Monday-start to Sunday-start week
                day_of_week = (day_of_week + 1) % 7  # 0 = Sunday, 6 = Saturday

                # get position for month grid
                month_x, month_y = month_coords[month]

                # calculate position of image in the month grid
                x = outer_margin + month_x * \
                    (month_width + month_spacing) + day_of_week * cell_width
                y = (20 * inch - outer_margin) - month_y * (month_height +
                                                            month_spacing) - (week_of_month * cell_height)

                # get full path for image
                png_file = os.path.join(png_directory, filename)

                # load and scale image
                img_reader = ImageReader(png_file)
                img_width, img_height = img_reader.getSize()

                # scale the image to fit within cell
                scale_x = cell_width / img_width
                scale_y = cell_height / img_height
                scale_factor = min(scale_x, scale_y)
                new_width = img_width * scale_factor
                new_height = img_height * scale_factor

                # draw image in correct position
                c.drawImage(img_reader, x, y - new_height,
                            width=new_width, height=new_height)

            except Exception as e:
                logging.error("Error processing %s: %s", filename, e)

    c.save()


if __name__ == '__main__':
    IMG_DIR = 'output/'
    YEAR = 2024
    OUTPUT_PDF = f'route-calendar-{YEAR}.pdf'
    draw_calendar_with_routes(OUTPUT_PDF, IMG_DIR, YEAR)
